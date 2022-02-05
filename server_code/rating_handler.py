import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_user_rating(site, user, new_rating):
  rating_row = app_tables.sites_rating.get(site=site, user=user)
  if not rating_row:
    app_tables.sites_rating.add_row(site=site, user=user, rating=new_rating)
  else:
    rating_row['rating'] = new_rating

@anvil.server.callable
def get_site_rating(site):
  total_rating = 0
  for row in app_tables.sites_rating.search(site=site):
    total_rating += {True: 1, False: -1}[row['rating']]
  return total_rating