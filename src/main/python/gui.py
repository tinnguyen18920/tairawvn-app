#import fbs's modules
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property


#import Pyqt5's modules
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox, QFileDialog
)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread

#Import ui files
from ui.mainwindow import Ui_MainWindow

#Built-in import
from urllib.parse import urlparse
import os

#Modules import
from raws import *
import raws
MAPPING = {}
for module in raws.__all__:
    class_ = "raws" + "." + module + "." + module.title()
    real_class = eval(class_)
    for netloc in real_class.NETLOC_LIST:
        MAPPING.setdefault(netloc, real_class)
from modules import requests, merge

class AppContext(ApplicationContext):
    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MainWindow()


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center()
        self.setupUi(self)
        self.folder_button.hide()
        self.quit_button.hide()
        self.setWindowTitle("TaiRawVN - v1.1")
        self.ui_data()
        self.mapping()

    def center(self):
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.sc_height = self.screenRect.height()
        self.sc_width = self.screenRect.width()
        self.resize(self.sc_width*2/3 - 100, self.sc_height*2/3 - 100)


    def ui_data(self):
        """
        Add data to GUI
        """
        # print(dir(self.list_supported))
        self.list_supported.addItems(MAPPING.keys())

        
        # self.list_supported.addItems([str(i) for i in range(2,2000)])

    def mapping(self):
        """
        Mapping between components and actions gui
        """
        self.download_button.clicked.connect(self.download_button_clicked)
        # self.cancel_button.clicked.connect(self.cancel_button_clicked)
        # self.quit_button.clicked.connect(self.quit_button_clicked)
        self.files_button.clicked.connect(self.merge_clicked_files)
        # self.folder_button.clicked.connect(self.merge_clicked_folder)


    #TODO: ADD IS_RUNNING, ADD disable others button
    def merge_clicked_files(self):
        image_files = QFileDialog.getOpenFileNames(self, "Chọn hình ảnh để ghép", filter="Common Images (*.jpg *.jpeg *.png);; Web Image(*.webp)")
        # print(image_files)?
        if image_files[0]:
            self.merge_thread = MergeThread(image_files[0])
            self.merge_thread.finished.connect(self.save_canvas)
            self.start_merge()
            self.merge_thread.start()
            IS_RUNNING = 1  
            
    def merge_clicked_folder(self):
        folder_path = (QFileDialog.getExistingDirectory(self, "Chọn thư chứa hỉnh ảnh muốn ghép raw"))
        print(folder_path)

    def save_canvas(self):
        # if MERGE_RESULT:
        merge_status = MERGE_RESULT.get("status")

        if merge_status == "error":
            self.show_dialog(MERGE_RESULT.get("msg"))
            self.done_save_canvas()
        else:
            canvas_path = QFileDialog.getSaveFileName(self, "Chọn chỗ lưu ảnh đã ghép raw", filter="PNG (*.png)")
            self.save_canvas_thread = SaveCanvasThread(MERGE_RESULT.get("canvas"), canvas_path[0])
            # self.save_canvas_thread.finished.connect(self.done_save_canvas)
            self.save_canvas_thread.start()
            # CANVAS.save(canvas_path[0])

        self.done_save_canvas()
    def start_merge(self):
        self.files_button.setEnabled(False)
    def done_save_canvas(self):
        self.files_button.setEnabled(True)

    def download_button_clicked(self):
        """        """
        url = self.url_input.text()
        if not url:
            message = "Vui lòng nhập link chap"
            # title = ""
            self.show_dialog(message=message)
        else:

            #Disable Download button
            self.start_download()
            self.IS_RUNNING = 1
            self.download_thread = DownloadThread(url)
            self.download_thread.finished.connect(self.donwload_finished)
            self.download_thread.start()


    def donwload_finished(self):
        # print(DOWNLOAD_RESULT)
        status = DOWNLOAD_RESULT.get("status")
        if status.lower() == "error":
            error_msg = DOWNLOAD_RESULT.get("msg")
            if error_msg.lower() == "need buy episode":
                error_msg = "Chưa hổ trợ tải chap có tính phí"
            self.show_dialog(message=error_msg)
        elif DOWNLOAD_RESULT.get("POOL_RES"):
            folder_path = str(QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu raw"))
            #TODO: Handler QFileDialog
            pool_res = DOWNLOAD_RESULT.get("POOL_RES")
            self.save_thread = SaveThread(folder_path, pool_res)
            self.save_thread.finished.connect(self.save_finished)
            self.save_thread.start()

        self.download_done()

    def start_download(self):
        self.download_button.setEnabled(False)

    def download_done(self):
        self.download_button.setEnabled(True)
        self.url_input.clear()


    def save_finished(self):
        #TODO: Add something action when images was saved: notification, open folder, save data, congratulation
        self.IS_RUNNING = 0

    def cancel_button_clicked(self):
        pass


    def quit_button_clicked(self):
        pass


    def show_dialog(self, message, title="Info"):
        """
        Referenced from https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message.title())
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle(title)
        # msg.setDetailedText("The details are as follows:")
        # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msg.buttonClicked.connect(msgbtn)
        self.IS_RUNNING = 0
        msg.exec_()


    def closeEvent(self, event):
        if self.IS_RUNNING == 1:
            close = QMessageBox.question(self,
                                     "QUIT",
                                     "Dừng quá trình tải raw và thoát ?",
                                     QMessageBox.Yes | QMessageBox.No)
        
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        


class DownloadThread(QThread):
    """
    Thread get all images from chap (RAW)
    """
    def __init__(self, url):
        QThread.__init__(self)
        self._url = url

    def run(self):
        global DOWNLOAD_RESULT
        self.netloc_input = urlparse(self._url).netloc
        raw_class = MAPPING.get(self.netloc_input, False)
        if not raw_class:
            DOWNLOAD_RESULT = {"status": "error", "msg": "not supported %s" % self.netloc_input}
            return False
        else:

            try:
                data = raw_class.main(self._url)
            except:
                DOWNLOAD_RESULT = {"status" : "error", "msg" : "%s đã thay đổi cách tải raw. Vui lòng liên hệ Admin để đề nghị cập nhật. Erro_Code: 173" % self.netloc_input}
                return False

            data_status = data.get("status")
            if data_status == "error":
                DOWNLOAD_RESULT = data
            else:
                # self.guidownload = GuiDownload(raw_class, url)
                # self.guidownload.finished.connect(self.download_pool)
                # # self.guidownload.test.connect(self.show_dialog())
                # self.download_button.setEnabled(False)
                # # self.cancle_button.setEnabled(True)

                # self.guidownload.start()
                self.download_images(data)

    def download_images(self, data):
        download_data = data.get("data")
        platform = download_data['platform']
        referer = download_data.get("referer", None)
        dler = requests.Downloader(platform=platform, referer=referer)

        global DOWNLOAD_RESULT
        try:
            pool_res = dler.pool_download(download_data['images'])
            DOWNLOAD_RESULT = {"status": "ok", "POOL_RES": pool_res}
        except requests.DownloadImageException:
            DOWNLOAD_RESULT = {"status" : "error", "msg" : "%s đã thay đổi cách tải raw. Vui lòng liên hệ Admin để đề nghị cập nhật. Erro_Code: 185" % self.netloc_input}
            return False


class SaveThread(QThread):
    """
    Save images from requests.pool_download to folder
    TODO: Handle missing image (response = False)
    """
    def __init__(self, folder_path, pool_res):
        QThread.__init__(self)
        self._folder_path = folder_path
        self._pool_res = pool_res

    def run(self):
        os.makedirs(self._folder_path, exist_ok=True)
        for pd in self._pool_res:
            file_name = pd['name'] + "." + pd['response'].headers.get("Content-Type").split("/")[-1]
            with open(self._folder_path + "/" + file_name, 'wb',) as file:
                file.write(pd['response'].content)


class MergeThread(QThread):
    """"""

    def __init__(self, image_files):
        QThread.__init__(self)
        self._images = image_files


    def run(self):
        global MERGE_RESULT
        m = merge.Merge(self._images)

        # try:
        canvas = m.merge()
        MERGE_RESULT = {"status" : "ok", "canvas": canvas}
        # except:
            # MERGE_RESULT = {"status" : "error", "msg": "cannot merege images"}

class SaveCanvasThread(QThread):
    def __init__(self, canvas, file_path):
        QThread.__init__(self)
        self._canvas = canvas
        self._file_path = file_path

    def run(self):
        self._canvas.save(self._file_path, "PNG")