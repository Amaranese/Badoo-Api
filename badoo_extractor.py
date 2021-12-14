from robobrowser import RoboBrowser
import re

BASE_URL = "https://badoo.com{}"

class BadooApi:

    def __init__(self):
        self.browser = RoboBrowser(history=True, parser='html.parser')
        self.browser.open(BASE_URL.format("/es/contactos/spain/madrid/madrid/"))

    def next_page(self):
        btns = self.browser.find_all(class_ =re.compile(r".*btn.*btn--xsm.*btn--transparent.*js-pages.*"))
        try:
            print(BASE_URL.format(btns[1]['href']))
            self.browser.open(BASE_URL.format(btns[1]['href']))
        except:
            print(BASE_URL.format(btns[0]['href']))
            self.browser.open(BASE_URL.format(btns[0]['href']))

    def extract_users(self):
        profiles = []
        for a in self.browser.find_all("a", {"rel":"profile-view"}):
            profiles.append({"url": a["href"],
                             "name": a["title"]})
        return profiles

    def get_public_profile(self, url):
        self.browser.open(BASE_URL.format(url))
        photos = []
        for img in self.browser.find_all(class_ = re.compile(r'.*photo-list__img.*js-gallery-img.*')):
            photos.append(img['src'])
        info = self.browser.find("title").text.split("|")
        personal_info = info[0].split(",")
        name = personal_info[0]
        sex = personal_info[1]
        age = personal_info[2]
        location = info[1]
        return ({"name":name,
                "sex": sex,
                "age": age,
                "location": location,
                "photos":photos})