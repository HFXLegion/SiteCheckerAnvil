from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..string import String
from ..content_manager import ContentManager

# A homepage class
class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #anvil.users.login_with_form()
    
  # Function for reset labels and icons
  def clear_content(self):
    # Clear icons
    self.database_check_image.source = None
    self.ai_check_image.source = None
    self.rating_check_image.source = None
    self.users_rating_image.source = None
    
    # Set loading status for labels
    self.database_check_label.text = "Поиск сайта в базе данных..."
    self.ai_check_label.text = "Проверка содержимого страницы..."
    self.rating_check_label.text = "Проверка отзывов сайта..."
    self.users_rating_text.text = "Составление рейтинга сайта..."
    
    # Hide rating elements
    self.rate_this_site.visible = False
    self.like.visible = False
    self.dislike.visible = False
    self.smile.visible = False
    self.thanks.visible = False
    
  # Get logged user
  def get_user(self):
    if anvil.users.get_user() is None:
      return anvil.users.login_with_form()
    else:
      return anvil.users.get_user()
    
  def __process_site_checking(self, url, site):
    # Don't show loading bar
    with anvil.server.no_loading_indicator:
      database = anvil.server.call('database_check', url)
    if database < 75:
      self.database_check_image.source = ContentManager.get_good_icon()
      self.database_check_label.text = "Сайт не пытается быть похожим на популярный"
    elif database > 75:
      self.database_check_image.source = ContentManager.get_bad_icon()
      self.database_check_label.text = "Сайт пытается быть похожим на популярный"
    
    # Don't show loading bar
    with anvil.server.no_loading_indicator:
      try: # Try to het site HTML
        content = anvil.server.call('content_check', url)
      except: # If an error occureed when requesting
        self.clear_content()
        self.database_check_label.text = "Ошибка при выполнении запроса"
        self.database_check_image.source = ContentManager.get_bad_icon()
        return
    if "casino" in content: # If site looks like casino
      self.ai_check_image.source = ContentManager.get_bad_icon()
      self.ai_check_label.text = "Сайт похож на казино"
    elif "scam" in content: # If site looks like scam
      self.ai_check_image.source = ContentManager.get_bad_icon()
      self.ai_check_label.text = "Сайт похож на лохотрон"
    elif "market" in content: # If site looks like market
      self.ai_check_image.source = ContentManager.get_good_icon()
      self.ai_check_label.text = "Сайт похож на интерент-магазин"
    elif "search" in content: # If site looks like searching system
      self.ai_check_image.source = ContentManager.get_good_icon()
      self.ai_check_label.text = "Сайт похож на поисковую систему"
    elif "conn_err" in content: # If domain returns an error
      self.ai_check_label.text = "Сайт принудительно разорвал соединение"
      self.ai_check_image.source = ContentManager.get_warning_icon()
    else: # If system can't detect site type
      self.ai_check_image.source = ContentManager.get_warning_icon()
      self.ai_check_label.text = "Системе не удалось определить тип сайта"
    
    # Don't show loading bar
    with anvil.server.no_loading_indicator:
      # Check online rating
      rate = anvil.server.call('rating_check', site)
    if rate == -1: # If site have no rating
      self.rating_check_image.source = ContentManager.get_warning_icon()
      self.rating_check_label.text = "У сайта нет отзывов"
    elif rate < 3.5: # If rating is bad
      self.rating_check_image.source = ContentManager.get_bad_icon()
      self.rating_check_label.text = f"У сайта плохие отзывы ({rate} из 5)"
    elif rate >= 3.5: # If rating is good
      self.rating_check_image.source = ContentManager.get_good_icon()
      self.rating_check_label.text = f"У сайта хорошие отзывы  ({rate} из 5)"
    
    # Don't show loading bar
    with anvil.server.no_loading_indicator:
      # Get community rating
      site_rating = anvil.server.call('get_site_rating', site)
    self.users_rating_text.text = f"Рейтинг сайта: {site_rating}"
    if not site_rating: # If no rating
      self.users_rating_image.source = ContentManager.get_warning_icon()
    elif site_rating > 0: # If site have a good rating
      self.users_rating_image.source = ContentManager.get_good_icon()
    elif site_rating < 0: # If site have a bad rating
      self.users_rating_image.source = ContentManager.get_bad_icon()
    
  # If user clicks process button
  def process_checking_click(self, **event_args):
    self.clear_content() # Refresh content
    
    # Get url, site and domain by input
    url, site, _ = String.fit_url(self.url_entry.text)
    
    self.__process_site_checking(url, site)
      
    # Show rating widgets
    self.rate_this_site.visible = True
    self.like.visible = True
    self.dislike.visible = True
    
  # Rate current site
  def __rate_site(self, rate):
    current_user = self.get_user()
    site = String.fit_url(self.url_entry.text)[1]
    with anvil.server.no_loading_indicator:
      anvil.server.call('add_user_rating', site, current_user, rate)
    self.smile.visible = True
    self.thanks.visible = True
    
  # If user clicks "Like" button
  def like_click(self, **event_args):
    self.__rate_site(True)

  # If usel clicks "Dislike" button
  def dislike_click(self, **event_args):
    self.__rate_site(False)


