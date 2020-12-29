#00:49 29-12-2020

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Weibo:
    NAME = "Weibo"
    PLATFORM = "pc"
    NETLOC_LIST = ["manhua.weibo.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        request_url = "https://apiwap.vcomic.com/wbcomic/comic/comic_play"
        params = {
            "chapter_id": chap_id,
            "_request_from": "pc"
        }
        data = self.requests.json(url=request_url, method="get", params=params)
        if not data:
            return response['request_url_error']

        if not data['data']['chapter']:
            return response['not_found']
        # elif:
        #     return response['not_found']


        images = []
        
        try:
            # Logic for scrape images -> append to "images"
            images = [img.get("newImgUrl", img.get("mobileImgUrl"))  for img in data['data']['json_content']['page']]
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("p/(\d+?)/", path, re.I).group(1)
        except AttributeError:
            return response["invalid_url"]

        return Weibo().images(chap_id)