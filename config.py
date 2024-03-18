import os

file_warehouse = './warehouse.csv'
file_sold_items = './sold.csv'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY") or "remember-to-add-secret-key"
   SQLALCHEMY_DATABASE_URI = (
           os.environ.get('DATABASE_URL') or
           'sqlite:///' + os.path.join(BASE_DIR, 'warehouse.db')
   )
   SQLALCHEMY_TRACK_MODIFICATIONS = False