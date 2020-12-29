#11:13 29-12-2020

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Kuainkanmanhua:
    NAME = "Kuainkanmanhua"
    PLATFORM = "mobile"
    NETLOC_LIST = ["m.kuaikanmanhua.com", "www.kuaikanmanhua.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        chap_url = "https://m.kuaikanmanhua.com/mobile/comics/%s/" % chap_id
        soup = self.requests.soup(url=chap_url, method="get")
        if not soup:
            return response['request_url_error']

        # if soup:
        #     return response['need_buy']
        # elif soup:
        #     return response['not_found']

        
        images = []
        
        try:
            #Logic for scrape images -> append to "images"
            container = soup.find("div", {"class":"ComicPics comic-pics"})
            images_ele = container.findAll("img")
            for img in images_ele:
                img_url = img['data-src']
                img_url.replace("amp;", "")

                images.append(img_url)
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM, "referer": chap_url}}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("/(comic|comics)/(\d+)/", path, re.I).group(2)
        except AttributeError:
            return response["invalid_url"]

        return Kuainkanmanhua().images(chap_id)