from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http as requests
import re
from html.parser import HTMLParser as HTMLParserBase


class HTMLParser(HTMLParserBase):
    def handle_starttag(self, tag: str, attrs) -> None:
      if self.class_ != None:
        for attribute in attrs:
          if attribute[0] == "class" and attribute[1] == self.class_:
            self.__on_tag = True
            break
        else:
          if tag in self.tags:
              self.__on_tag = True
        return super().handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self.__on_tag:
            self.container.append(data)
            self.__on_tag = False
        return super().handle_data(data)

    def handle_endtag(self, tag: str) -> None:
        self.__on_tag = False
        return super().handle_endtag(tag)

    def get_tags_content(self, html, tags=(), class_=None):
        self.class_ = class_
        self.__on_tag = False
        self.container = list()
        if not isinstance(tags, (tuple, list)):
            tags = (tags)
        self.tags = tags
        super().feed(html)
        return self.container


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

    def find_all(self, tags=(), class_=None):
        return HTMLParser().get_tags_content(self.html, tags, class_)

    def get_headers(self):
        return self.find_all(("h1", "h2", "h3", "h4", "h5", "h6"))

    def get_main_text(self):
        return self.find_all(("title", "strong", "p", "h1", "h2", "h3", "h4", "h5", "h6"))

    def get_all_text(self):
        return self.find_all(("a", "title", "p", "ul", "li", "div", "span", "strong", "h1", "h2", "h3", "h4", "h5", "h6"))

