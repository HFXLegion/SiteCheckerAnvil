import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .string import String
from .site_parser import SiteParser


# Method for checking site domain in database
@anvil.server.callable
def database_check(url):
    url, site, domain = String.fit_url(url)
    biggest_similatiry = 0  # Define integer var for biggest similarity with popular sites
    for site_ in app_tables.sites_rating.search():  # Iter sites database
      site_ = site_["site"].strip()  # Remove spaces and new lines in site domain
      # Set biggest similarity max value between site similarity ratio and biggest similarity
      biggest_similatiry = max(String.get_similarity(site_, site), biggest_similatiry)
      if site_ == url or biggest_similatiry == 100:  # If site full matches to current
          return 0  # This site is in database
    return biggest_similatiry

# Method for checking site content
@anvil.server.callable
def content_check(url):
    url, site, domain = String.fit_url(url)
    # Combine text of all main web page tags
    main_text = ", ".join(SiteParser(url).get_main_text().get_tags_text()).lower()
    print(main_text)
    total = set()  # Define set for trigger words
    for row in app_tables.trigger_words.search():
      if row['word'] in main_text:
        total.add(row['response'])
    return tuple(total)  # Return tuple of trigger words

# Method for checking site rating
@anvil.server.callable
def rating_check(url):
    url, site, domain = String.fit_url(url)
    url = "https://www.mywot.com/scorecard/" + site  # Define URL with site rating
    try:  # Try to get rating value
        rating = float(SiteParser(url).get_tags("div")[0].text)
    except IndexError:  # If site have no rating
        return -1
    else:
        return rating
