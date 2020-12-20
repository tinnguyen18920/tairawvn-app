import json, re
from urllib.parse import urlparse, parse_qs

#
from modules import requests

class Bilibili:
    PLATFORM = "mobile"
    NETLOC_LIST = ["manga.bilibili.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id):
        payload = {"ep_id": chap_id}
        payload = json.dumps(payload)
        params = {
            "device": "h5",
            "platform": "web"
        }
        

        data = self.requests.json("https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex", 
            data=payload, params=params, method="post")
        if not data:
            return {"status": "error", "msg": "cannot download webpage"}
        
        #TODO: add same size
        # https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken

        res_code = data['code']
        if res_code == 1:
            return {"status": "error", "msg": data["msg"]}
        elif res_code == 'invalid_argument':
            return {"status": "error", "msg": "Chap not found"}
        
        urls = [image['path'] for image in data['data']['images']]
        urls_dumped = json.dumps(urls)
        urls_payload = json.dumps({"urls": urls_dumped})
        real_data = self.requests.json("https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken", 
                                    method="post",
                                    params=params,
                                    data=urls_payload
            )
        images = [image['url']+"?token="+image['token'] for image in real_data['data']]
        

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("/(\d+)/$", path, re.I).group(1)
            return Bilibili().images(chap_id)
        except AttributeError:
            return {"status": "error", "msg": "invalid bilibili url"}