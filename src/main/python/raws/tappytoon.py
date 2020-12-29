#00:55 29-12-2020

#Built-in
import json, re
from urllib.parse import urlparse, parse_qs

#Local
from modules import requests
from modules.exceptions import response

#Internet

class Tappytoon:
    NAME = "Tappytoon"
    PLATFORM = "pc"
    NETLOC_LIST = ["www.tappytoon.com"]
    def __init__(self):
        self.requests = requests.TairawRequests(self.PLATFORM)

    def images(self, chap_id) -> dict():
        
        request_url = "https://api-global.tappytoon.com/chapters/%s" % chap_id
        params = {
            "includes": "pagination,tracker_label,images",
            "locale": "en",
        }

        """
        Request(method='GET', url='https://api-global.tappytoon.com/chapters/710940678?includes=pagination,tracker_label,images&locale=en', headers={'Host': 'api-global.tappytoon.com', 'Connection': 'keep-alive', 'Accept': 'application/json', 'X-Device-Uuid': '0d740b8c-af7f-4fa8-936b-a30e88330bac', 'Authorization': 'Bearer JuCdEk6JboUSNQV6IScQZYc2yHAfRj4II/oiX/VAwPYmeBwqq6vG8nvRSOOWj/T1nDktysOfWxOZ7xtm8jyrF/DZP/PRWufGcrApLyP1srsYKdh2uh6A60auTaDsLXRr', 'Accept-Language': 'en', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'Origin': 'https://www.tappytoon.com', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://www.tappytoon.com/en/chapters/710940678?', 'Accept-Encoding': 'gzip, deflate, br'}, body=b'')
        """
        header = {
            "Authorization" : "Bearer JuCdEk6JboUSNQV6IScQZYc2yHAfRj4II/oiX/VAwPYmeBwqq6vG8nvRSOOWj/T1nDktysOfWxOZ7xtm8jyrF/DZP/PRWufGcrApLyP1srsYKdh2uh6A60auTaDsLXRr",
            "Referer": "https://www.tappytoon.com/",
            # "x-device-uuid" : "385d4e6f-0a11-4b9d-802f-9b47f03a00e1"
        }
        self.requests.update_header(header)

        data = self.requests.json(url=request_url, method="get", params=params)
        if not data:
            return response['request_url_error']

        
        status = str(data.get("status")) 
        if status == "400":
            return response['not_found']
        elif status == "403":
            return response['not_logged_in']

        
        images = []
        
        try:
            #Logic for scrape images -> append to "images"
            images = [img['url'] for img in data['images']]
        except:
            return response['site_changed']

        return {"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("chapters/(\d+)", path, re.I).group(1)
        except AttributeError:
            return response["invalid_url"]

        return Tappytoon().images(chap_id)