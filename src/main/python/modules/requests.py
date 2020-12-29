from requests import Session
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool



class DownloadImageException(Exception):
    pass

class TairawSession(Session):
    ''''''
    def __new__(self, platform):
        AGENTS = {
           "MOBILE": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
            "PC": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }
        session = Session()
        session.headers.update({"User-Agent": AGENTS.get(platform.upper())})
        return session


class TairawRequests:
    ''''''
    def __init__(self, platform):
        self._session = TairawSession(platform)


    def soup(self, url:str , **kwargs):
        ''''''
        try:
            response = self._session.request(url=url, **kwargs)
        except:
            # return {"status" : "fail", "msg": ""}
            raise RequestException

        try:
            soup = BeautifulSoup(response.text, "lxml")
        except:
            soup = False

        return soup


    def json(self, url: str, **kwargs):
        ''''''
        self._session.headers.update({'Content-Type' : 'application/json'})
        try:
            response = self._session.request(url=url, **kwargs)
        except:
            # return {"status" : "fail", "msg": ""}
            raise RequestException
        
        try:
            json_response = response.json()
        except:
            json_response = False

        return json_response


    def update_header(self, header):
        self._session.headers.update(header)
        
class Downloader:
    def __init__(self, platform, referer=None):
        self._session = TairawSession(platform)
        if referer:
            self._session.headers.update({"Referer": referer})
        self.pool = ThreadPool(cpu_count() * 2)

    def download_image(self, item: tuple) -> dict or False:
        """
        :param item: (image_index, image_url)
        :return: {"name": image_index, "response" : requests.models.Response} or False
        """
        image_index, image_url = item
        try:
            response = self._session.request(url=image_url, method="get")
        except:
            response = False
            # raise DownloadImageException
        return {"name": str(image_index), "response": response}

    def pool_download(self, images: list) -> list:
        """
        Download list of images by threads.
        :param images: ["https://image1.com", "https://image2.com"]
        :return:
        """
        result = self.pool.map(self.download_image, enumerate(images))
        return result