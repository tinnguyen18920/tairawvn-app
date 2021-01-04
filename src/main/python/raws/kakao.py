#10:27 03-01-2021

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Kakao:
    NAME = "Kakao"
    PLATFORM = "pc"
    NETLOC_LIST = ["page.kakao.com", "channel-page.kakao.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        request_url = "https://api2-page.kakao.com/api/v1/inven/get_download_data/web"
        params = {
            'productId': str(chap_id), 
            'device_mgr_uid': 'Windows - Chrome', 
            'device_model': 'Windows - Chrome', 
            # 'deviceId': '2d6330f380f44ac20f3a02eed0958f66'
        }
        data = self.requests.json(url=request_url, method="post", params=params)
        if not data:
            return response['request_url_error']

        status_code = str(data.get("result_code"))
        if status_code == "-500":
            return response['not_found']
        elif status_code == "-110":
            return response["not_logged_in"]
        elif status_code == "-205":
            return {"status": "error", "msg": "Ad chưa thể tải chap chỉ có trên ứng dụng"}
        elif status_code != "0":
            return {"status": "error", "msg": "Lỗi chưa biết :3"}
        
        # elif:
        #     return response['not_found']


        images = []
        
        try:
            #Logic for scrape images -> append to "images"
            server = data.get("downloadData")['members']['sAtsServerUrl']
            for file in data.get("downloadData")['members']['files']:
                img_url = server + file['secureUrl']
                images.append(img_url)
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        qs = urlparse(url).query
        # if not path.endswith("/"):
            # path += "/"
        try:
            chap_id = parse_qs(qs).get("productId", "")[0]
        except IndexError:
            return response["invalid_url"]
        except AttributeError:
            return response["invalid_url"]

        return Kakao().images(chap_id)