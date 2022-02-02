import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.server

@anvil.server.callable
def add_user(article_dict):
  current_user = anvil.users.get_user()
  if current_user is not None:
    app_tables.articles.add_row(content=None, title="Main Row", user=current_user, **article_dict)

