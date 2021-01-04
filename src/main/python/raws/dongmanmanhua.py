#21:58 04-01-2021

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs, urlunparse

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Dongmanmanhua:
    NAME = "Dongmanmanhua"
    PLATFORM = "pc"
    NETLOC_LIST = ["m.dongmanmanhua.cn", "dongmanmanhua.cn", "www.dongmanmanhua.cn"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, url) -> dict():
        
        chap_url = url
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
            container = soup.find("div", {"id": "_imageList"})
            if not container:
                return response['not_found']
            img_eles = container.findAll("img")
            for img in img_eles:
                img_url = img['data-url']
                images.append(img_url)
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM, "referer": url}}

    @staticmethod
    def main(url):
        parsed = urlparse(url)
        parsed._replace(netloc="www.dongmanmanhua.cn")
        # if not path.endswith("/"):
        #     path += "/"
        # try:
        #     chap_id = re.search("", path, re.I).group(1)
        # except AttributeError:
        #     return response["invalid_url"]

        return Dongmanmanhua().images(url=urlunparse(parsed))