#11:03 03-01-2021

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Comicnaver:
    NAME = "Comicnaver"
    PLATFORM = "mobile"
    NETLOC_LIST = ["m.comic.naver.com", "comic.naver.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self,comic_id, chap_id) -> dict():
        
        chap_url = "https://m.comic.naver.com/webtoon/detail.nhn"
        params = {
            "titleId": str(comic_id),
            "no": str(chap_id)
        }
        soup = self.requests.soup(url=chap_url, method="get", params=params)
        if not soup:
            return response['request_url_error']

        
        images = []
        
        try:
            #Logic for scrape images -> append to "images"
            img_eles = soup.findAll("img", {"class":"fx2 lazy"})
            if not img_eles:
                return response['not_found']
            for ele in img_eles:
                images.append(ele['data-src'])
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        qs = urlparse(url).query
        # if not path.endswith("/"):
            # path += "/"
        try:
            comic_id = parse_qs(qs).get("titleId")[0]
            chap_id = parse_qs(qs).get("no")[0]
        except IndexError:
            return response["invalid_url"]
        except AttributeError:
            return response["invalid_url"]

        return Comicnaver().images(comic_id=comic_id, chap_id=chap_id)