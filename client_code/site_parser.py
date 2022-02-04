from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http as requests
import re
from html.parser import HTMLParser

@anvil.server.portable_class
class SiteParser:
    class Tag:
        def __init__(self, tag, body):
            self.tag = tag
            self.text = body[body.find(f"{tag}>")+1:tag.find(f"</{tag}")-1]

    class Tags(list):
        def __init__(self, tags=()):
            super().__init__(tags)

        def get_tags_text(self):
            for tag in self:
                yield tag.text

    def __init__(self, url):
        self.html = requests.request(self.fit_url(url)[0]).get_bytes().decode()

    @staticmethod
    def fit_url(url):
        if not url.startswith("http"):
            protocol = "https://"
        else:
            protocol = url.split("//")[0] + "//"
        url = url.replace("http://", "").replace("https://", "").replace("www.", "")
        site = url.split("/")[0].strip()
        return (protocol + url), site, (protocol + site)

    def find_all(self, tags=()):
        tags_container = self.Tags()
        if isinstance(tags, (tuple, list)):
            for tag in tags:
                tags_container.extend(self.find_all(tag))
        else:
            #print(re.findall(rf"<{tags}.*>.*</{tags}>", self.html))
            tags_container.extend(self.Tag(tags, x) for x in re.findall(rf"<{tags}.*>.*</{tags}>", self.html))
        return tags_container


    def get_headers(self):
        return self.find_all(("h1", "h2", "h3", "h4", "h5", "h6"))

    def get_main_text(self):
        return self.find_all(("title", "strong", "p", "h1", "h2", "h3", "h4", "h5", "h6"))

    def get_all_text(self):
        return self.find_all(("a", "title", "p", "ul", "li", "div", "span", "strong", "h1", "h2", "h3", "h4", "h5", "h6"))

