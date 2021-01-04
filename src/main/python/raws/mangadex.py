#11:48 03-01-2021

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Mangadex:
    NAME = "Mangadex"
    PLATFORM = "pc"
    NETLOC_LIST = ["mangadex.org"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        request_url = "https://mangadex.org/api/"
        params = {
            "id": str(chap_id),
            "type": "chapter"
        }
        data = self.requests.json(url=request_url, method="get", params=params)
        if not data:
            return response['request_url_error']

        status = data.get("status")
        if status == 'error':
            return {"status": "error", "msg": data.get("message")}
        # elif:
        #     return response['not_found']


        images = []
        
        try:
            #Logic for scrape images -> append to "images"
            server = data.get("server") + data.get("hash") + "/"
            for img in data.get("page_array"):
                img_url = server + img
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
            chap_id = re.search("chapter/(\d+?)/", path, re.I).group(1)
        except AttributeError:
            return response["invalid_url"]

        return Mangadex().images(chap_id)