"""
    Start a new site
"""
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

from modules import requests
# import sys

DATA = {}

cant = """{"status": "error", "msg": "cannot download webpage"}"""
not_found = """{"status": "error", "msg": "Chap not found"}"""
need_buy = """{"status": "error", "msg": "need buy episode"}"""
success = """{"status": "ok", "data": {"images": images, "platform": self.PLATFORM}}"""
invalid_url = """{"status": "error", "msg": "invalid url"}"""
BASE = """import json, re
from urllib.parse import urlparse, parse_qs

#
from modules import requests

class {class_name}:
    PLATFORM = "{platform}"
    NETLOC_LIST = ["{netloc}"]
    def __init__(self):
        self.requests = requrests.TairawRequests(self.PLATFORM)

    def images(self, chap_id):
        chap_url = "" % chap_id
        soup = self.requests.soup(url=chap_url, method="get")
        if not soup:
            return {cant}

        if soup:
            return {not_found}
        elif soup:
            return {need_buy}

        #Logic to find images
        images = 
        return {success}

    @staticmethod
    def main(url):
        path = urlparse(url).path
        if not path.endswith("/"):
            path += "/"
        try:
            chap_id = re.search("/(\d+)/$", path, re.I).group(1)
            return Bilibili().images(chap_id)
        except AttributeError:
            return {invalid}"""

def write_soup(html_file_name, example):
    with open("%s\\%s.html" % ("raws", html_file_name ), "w", encoding="utf-8") as soup_file:
        soup_file.write(example)

def write_python(py_file_name, platform, netloc):
    BASE_ = BASE.format(class_name=file_name.title(), platform=platform, netloc=netloc,                    cant=cant,
                    not_found=not_found,
                    need_buy=need_buy,
                    success=success,
                    invalid=invalid_url)
    with open("%s\\%s.py" % ("raws", py_file_name), "w", encoding="utf-8") as py_file:
        py_file.write(BASE_)

def main():
    global file_name
    file_name = input("File name (.py): ")
    file_name = file_name.lower()


    chap_url = input("CHAP_URL: ")
    PLATFORM_LIST = ["mobile", "pc"]
    for platform in PLATFORM_LIST:
        current_requests = requests.TairawSession(platform)

        print("Prepare download page in %s agent" % platform.upper())
        response = current_requests.request(method="get", url=chap_url)
        # import pdb; pdb.set_trace()
        print("\tIs redirect : %s" % str(response.is_redirect))
        response_size = len(response.content)
        current_url = response.url
        current_netloc = urlparse(current_url).netloc
        soup = BeautifulSoup(response.text , "lxml")
        try:
            total_image_body = len(soup.body.find_all("img"))
        except:
            total_image_body = -1

        print("\tSize: %s | Total images in body : %s" % (str(response_size), str(total_image_body) ))

        DATA.setdefault(platform, {"example" : soup.prettify(), "netloc": current_netloc})

    choose = input("What you choose %s or 'all' : " % " or ".join(PLATFORM_LIST)).lower()
    # choose = choose.lower()

    # os.makedirs(file_name, exist_ok= True)
    if choose == "all":
        for key, value in DATA.items():
            write_soup("%s_%s" % (file_name, key), value.get("example"))
            write_python("%s_%s" % (file_name, key), platform=key, netloc=value.get("netloc"))
    else:

        write_soup("%s" % file_name, DATA.get(choose).get("example"))
        write_python("%s" % file_name, platform=choose, netloc=DATA.get(choose).get("netloc"))
if __name__ == '__main__':
    main()