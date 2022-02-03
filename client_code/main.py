import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from difflib import SequenceMatcher
from .modules.site_parser import SiteParser
from .modules.string import String

# Main script for checking websites content, rating and database
class SiteChecker:
    RATING_SITE = "https://www.mywot.com/scorecard/"  # Website for checking other sites rating

    def __init__(self, url, url_database_path: str):
        self.url_database_path = url_database_path
        self.__url, self.__site, self.__domain = String.fit_url(url)

    # Method for checking site domain in database
    def database_check(self):
        with open(self.url_database_path, "r") as sites:  # Open database with read mode
            biggest_similatiry = 0  # Define integer var for biggest similarity with popular sites
            for site in sites.readlines():  # Iter sites database
                site = site.strip()  # Remove spaces and new lines in site domain
                # Set biggest similarity max value between site similarity ratio and biggest similarity
                biggest_similatiry = max(SequenceMatcher(None, site, self.__site).ratio(), biggest_similatiry)
                if site == self.__url or biggest_similatiry*100 == 100.0:  # If site full matches to current
                    return 0  # This site is in database

        return biggest_similatiry*100

    # Method for checking site content
    def content_check(self):
        # Combine text of all main web page tags
        main_text = ", ".join(SiteParser(self.__url).get_main_text().get_tags_text()).lower()
        total = set()  # Define set for trigger words
        for row in app_tables.trigger_words.search():
          if row['word'] in main_text:
            total.add(row['response'])
        return tuple(total)  # Return tuple of trigger words

    # Method for checking site rating
    def rating_check(self):
        url = self.RATING_SITE + self.__site  # Define URL with site rating
        try:  # Try to get rating value
            rating = float(SiteParser(url).get_tags("div")[0].text)
        except IndexError:  # If site have no rating
            return -1
        else:
            return rating
