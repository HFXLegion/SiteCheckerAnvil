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
    
  def clear_icons(self):
    self.database_check_image.source = None
    self.ai_check_image.source = None
    self.rating_check_image.source = None
    
  def clear_text(self):
    self.database_check_label.text = "Поиск сайта в базе данных..."
    self.ai_check_label.text = "Проверка содержимого страницы..."
    self.rating_check_label.text = "Проверка рейтинга сайта..."

  def process_checking_click(self, **event_args):
    self.clear_icons()
    self.clear_text()
    
    url, site, domain = String.fit_url(self.url_entry.text)
    
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
      
    content = anvil.server.call('content_check', url)
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
      
    rating = anvil.server.call('rating_check', site)
    if rating < 3.5:
      self.rating_check_label.text = f"У сайта низкий рейтинг ({rating} из 5)"
      self.rating_check_image.source = ContentManager.get_bad_icon()
    elif rating >= 3.5:
      self.rating_check_label.text = f"У сайта высокий рейтинг  ({rating} из 5)"
      self.rating_check_image.source = ContentManager.get_good_icon()
    