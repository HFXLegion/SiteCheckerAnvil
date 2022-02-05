from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..string import String
from ..content_manager import ContentManager


class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #anvil.users.login_with_form()

  def get_good_icon(self, **event_args):
    ContentManager.get_good_icon()
    
    
  def clear_content(self):
    self.database_check_image.source = None
    self.ai_check_image.source = None
    self.rating_check_image.source = None
    self.users_rating_image.source = None
    
    self.database_check_label.text = "Поиск сайта в базе данных..."
    self.ai_check_label.text = "Проверка содержимого страницы..."
    self.rating_check_label.text = "Проверка отзывов сайта..."
    self.users_rating_text.text = "Составление рейтинга сайта..."
    
    self.rate_this_site.visible = False
    self.like.visible = False
    self.dislike.visible = False
    self.smile.visible = False
    self.thanks.visible = False
    
  def check_user(self):
    if anvil.users.get_user() is None:
      return anvil.users.login_with_form()
    else:
      return anvil.users.get_user()
    

  def process_checking_click(self, **event_args):
    self.clear_content()
    
    url, site, domain = String.fit_url(self.url_entry.text)
    
    with anvil.server.no_loading_indicator:
      database = anvil.server.call('database_check', url)
    if not database:
      self.database_check_label.text = "Сайт является проверенным"
      self.database_check_image.source = ContentManager.get_good_icon()
    elif database < 75:
      self.database_check_label.text = "Сайт не быть похожим на популярный"
      self.database_check_image.source = ContentManager.get_good_icon()
    elif database > 75:
      self.database_check_label.text = "Сайт пытается быть похожим на популярный"
      self.database_check_image.source = ContentManager.get_bad_icon()
      
    with anvil.server.no_loading_indicator:
      try:
        content = anvil.server.call('content_check', url)
      except:
        self.clear_content()
        self.database_check_label.text = "Ошибка при выполнении запроса"
        self.database_check_image.source = ContentManager.get_bad_icon()
        return
    if "casino" in content:
      self.ai_check_label.text = "Сайт похож на казино"
      self.ai_check_image.source = ContentManager.get_bad_icon()
    elif "scam" in content:
      self.ai_check_label.text = "Сайт похож на лохотрон"
      self.ai_check_image.source = ContentManager.get_bad_icon()
    elif "market" in content:
      self.ai_check_label.text = "Сайт похож на интерент-магазин"
      self.ai_check_image.source = ContentManager.get_good_icon()
    elif "search" in content:
      self.ai_check_label.text = "Сайт похож на поисковую систему"
      self.ai_check_image.source = ContentManager.get_good_icon()
    elif "conn_err" in content:
      self.ai_check_label.text = "Сайт принудительно разорвал соединение"
      self.ai_check_image.source = ContentManager.get_warning_icon()
    else:
      self.ai_check_label.text = "Системе не удалось определить тип сайта"
      self.ai_check_image.source = ContentManager.get_warning_icon()
      
    with anvil.server.no_loading_indicator:      
      rate = anvil.server.call('rating_check', site)
    if rate < 3.5:
      self.rating_check_label.text = f"У сайта плохие отзывы ({rate} из 5)"
      self.rating_check_image.source = ContentManager.get_bad_icon()
    elif rate >= 3.5:
      self.rating_check_label.text = f"У сайта хорошие отзывы  ({rate} из 5)"
      self.rating_check_image.source = ContentManager.get_good_icon()
    
    with anvil.server.no_loading_indicator:
      site_rating = anvil.server.call('get_site_rating', site)
    self.users_rating_text.text = f"Рейтинг сайта: {site_rating}"
    if not site_rating:
      self.users_rating_image.source = ContentManager.get_warning_icon()
    elif site_rating > 0:
      self.users_rating_image.source = ContentManager.get_good_icon()
    elif site_rating < 0:
      self.users_rating_image.source = ContentManager.get_bad_icon()
      
    self.rate_this_site.visible = True
    self.like.visible = True
    self.dislike.visible = True
    

  def like_click(self, **event_args):
    current_user = self.check_user()
    site = String.fit_url(self.url_entry.text)[1]
    with anvil.server.no_loading_indicator:
      anvil.server.call('add_user_rating', site, current_user, True)
    self.smile.visible = True
    self.thanks.visible = True

  def dislike_click(self, **event_args):
    site = String.fit_url(self.url_entry.text)[1]
    current_user = self.check_user()
    with anvil.server.no_loading_indicator:
      anvil.server.call('add_user_rating', site, current_user, False)
    self.smile.visible = True
    self.thanks.visible = True


