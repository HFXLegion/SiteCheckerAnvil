from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #anvil.users.login_with_form()

  def get_good_icon(self, **event_args):
    ContentManager.get_good_icon()

  def process_checking_click(self, **event_args):
    print(anvil.server.call('content_check', self.url_entry.text))
