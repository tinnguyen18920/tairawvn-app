#11:39 03-01-2021

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Rawmangas:
    NAME = "Rawmangas"
    PLATFORM = "pc"
    NETLOC_LIST = ["rawmangas.net"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, comic_id, chap_id) -> dict():
        
        chap_url = "https://rawmangas.net/manga/{comic_id}/{chap_id}/".format(
                comic_id=comic_id, chap_id=chap_id
            )
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
            container = soup.find("div", {"class":"reading-content"})
            if not container:
                return response['not_found']
            img_eles = container.findAll("img")
            for ele in img_eles:
                img_url = ele['data-src']
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
            comic_id = re.search("manga/(.+?)/", path, re.I).group(1)
            chap_id = re.search("/(\d+|\d+-raw)?/$", path, re.I).group(1)
        except AttributeError:
            return response["invalid_url"]

        return Rawmangas().images(comic_id=comic_id, chap_id=chap_id)