#00:55 29-12-2020

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Manmanapp:
    NAME = "Manmanapp"
    PLATFORM = "pc"
    NETLOC_LIST = ["manmanapp.com", "www.manmanapp.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        chap_url = "https://manmanapp.com/comic/detail-%s.html" % chap_id
        soup = self.requests.soup(url=chap_url, method="get")
        if not soup:
            return response['request_url_error']

        if soup.find("div", {"class": "notFound"}):
            return response['not_found']
        elif "pay_end.jpg" in str(soup):
            return response['need_buy']
        # if soup:
        #     return response['need_buy']
        # elif soup:
        #     return response['not_found']

        
        images = []
        
        try:
        #     #Logic for scrape images -> append to "images"
            images_ele = soup.findAll("img", {"class":"man_img"})
            for img in images_ele:
                images.append(img['src'])
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("(\d+)\.html/$", path, re.I).group(1)
        except AttributeError:
            return response["invalid_url"]

        return Manmanapp().images(chap_id)