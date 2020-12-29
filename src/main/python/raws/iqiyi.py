#00:33 29-12-2020

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Iqiyi:
    NAME = "Iqiyi"
    PLATFORM = "pc"
    NETLOC_LIST = ["www.iqiyi.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        chap_url = "https://www.iqiyi.com/manhua/reader/%s.html" % chap_id
        soup = self.requests.soup(url=chap_url, method="get")
        if not soup:
            return response['request_url_error']

        if 'pay-title' in str(soup):
            return response['need_buy']
        # elif soup:
        #     return response['not_found']

        
        images = []
        
        try:
            #Logic for scrape images -> append to "images"
            container = soup.find("ul", {"class":"main-container"})
            if not container:
                return response['not_found']
            images_ele = container.findAll("img")
            for img in images_ele:
                try:
                    img_url = img['src']
                except:
                    img_url = img['data-original']

                images.append(img_url)
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("reader/(.+?)/", path, re.I).group(1)
            chap_id = chap_id.split(".html")[0]
        except AttributeError:
            return response["invalid_url"]

        return Iqiyi().images(chap_id)