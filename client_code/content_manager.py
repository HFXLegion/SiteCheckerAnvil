import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ContentManager:
  def get_good_icon(self, **event_args):
      return app_tables.content.get(id=0)["data"]
    
  def get_warning_icon(self, **event_args):
      return app_tables.content.get(id=1)["data"]
    
  def get_bad_icon(self, **event_args):
      return app_tables.content.get(id=2)["data"]
