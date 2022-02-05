import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ContentManager:
  @staticmethod
  def get_good_icon(**event_args):
      return app_tables.content.get(id=0)["data"]
  
  @staticmethod
  def get_warning_icon(**event_args):
      return app_tables.content.get(id=1)["data"]
  
  @staticmethod
  def get_bad_icon(**event_args):
      return app_tables.content.get(id=2)["data"]
