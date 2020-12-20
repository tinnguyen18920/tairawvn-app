from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class DifferWidths(Exception):
    """Two images with different width"""

class Merge:

    def __init__(self, images):
        images.sort()
        self._images = [Image.open(x) for x in images]
        self.widths, self.heights = zip(*(i.size for i in self._images))

        self.max_width = max(self.widths)
        self.total_height = sum(self.heights)
        # self.total = (0, 0)

    def merge(self):
        h_position = 0
        canvas = Image.new("RGB", (self.max_width, self.total_height))

        for image in self._images:
            # print(image)
            i_w, i_h = image.size
            canvas.paste(image, (0, h_position))
            h_position += i_h

        # canvas.save("test.png", "PNG")
        return canvas
    # def prepare(self):
    #     ''''''
    #     all_images = []
    #     for image in self._images:
    #         print(image)
    #         current_image = Image.open(image)
    #         c_width, c_height = current_image.size
    #         if not self.max_width:
    #             self.max_width = c_width
    #         else:
    #             print("max_width %s" % str(self.max_width))
    #             print("current_width %s" % str(c_width))
    #             if self.max_width != c_width:
    #                 raise DifferWidths

    #         self.total_height += c_height
    #         # self.pil_images.append(current_image)
    #         all_images.append(current_image)

    #     return all_images
    # def merge(self):

    #     #create blank image with all images height
    #     canvas = Image.new('RGB',(self.max_width, self.total_height), (250,250,250))
        

    #     #Loop paste every image to canvas
    #     canvas_c_height = 0
    #     for image_file in self._images:
    #         image = Image.open(image_file)
    #         img_w, img_h = image.size
    #         canvas.paste(image, (img_w, canvas_c_height))
    #         canvas_c_height += img_h 

    #     canvas.save("test.jpg")

    # def start(self):
    #     self.prepare()
    #     self.merge()
