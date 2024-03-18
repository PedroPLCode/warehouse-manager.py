from flask import flash
from app import db
from app.product import Product
from app.models import Item
from config import *
import datetime
import csv
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log")

def get_current_time_and_date():
    date_and_time = datetime.datetime.now()
    return date_and_time.strftime("%X %x")


def create_new_product_instance(name, quantity_in_stock, quantity_sold, unit, unit_price, product_index):
    return Product(name, quantity_in_stock, quantity_sold, unit, unit_price, product_index)


def item_already_in_db(item, items_from_db):  
    if not items_from_db: 
        return False
    for item_from_db in items_from_db:
        if items_match(item_from_db, item):
            return True
    return False


def items_match(item_one, item_two):
    return True if item_one.name.strip().lower() == item_two.name.strip().lower() else False


def update_existing_item(new_item, items):
    for item in items:
        if items_match(item, new_item):
            if not item_in_conflict_with_other_items(new_item, item):
                update_item_action(item, new_item)
                logging.info(f"Added {new_item.quantity_in_stock} "
                             f"{item.unit} {item.name} to warehouse.")
                 
                              
def update_item_action(item, new_item):
    item.quantity_in_stock = float(item.quantity_in_stock) + float(new_item.quantity_in_stock)
    db.session.add(item)
    db.session.commit()
    flash(f'Added {new_item.quantity_in_stock} {new_item.unit} '
          f'of {new_item.name} to warehouse.')
   
   
def item_in_conflict_with_other_items(item_one, item_two):
    if item_one.unit != item_two.unit or float(item_one.unit_price) != float(item_two.unit_price):
        flash(f'Diffrent unit or unit price. '
              f'Try add this product with diffrent name.')   
        return True
    return False
    
    
def add_new_item_to_db(item):
    new_item = Item(name=item.name, 
                    quantity_in_stock=item.quantity_in_stock, 
                    quantity_sold=item.quantity_sold,
                    unit=item.unit, 
                    unit_price=item.unit_price, 
                    index=item.product_index)
    db.session.add(new_item)
    db.session.commit()
    flash(f'{item.quantity_in_stock} {item.unit} {item.name} '
          f'succesfully added to warehouse')
    logging.info("New item added")
    
    
def item_found_in_db(product_name, database):
    for item in database:
        if product_name.strip() == item.name.strip():
            return True
    return False
    

def sell_items_from_warehouse(sell_item_name, sell_item_quantity, items):
    logging.info(f"Item to sell: {sell_item_name} quantity {sell_item_quantity}")
    for item in items:
        if (item.name).strip().lower() == sell_item_name.strip().lower():
            if float(item.quantity_in_stock) >= sell_item_quantity:
                sell_action(item, sell_item_name, sell_item_quantity, items)
                break
            else:
                handle_not_enough_items(item, sell_item_name, sell_item_quantity)
                break


def sell_action(item, sell_item_name, sell_item_quantity, items):
        
    item.quantity_in_stock = round(float(item.quantity_in_stock) - sell_item_quantity, 2)
    item.quantity_sold = item.quantity_sold + sell_item_quantity

    db.session.add(item)
    db.session.commit()
    
    logging.info(f"Item {sell_item_name} sold")     
    flash(f'{sell_item_quantity} {item.unit} {item.name} '
          f'succesfully sold from warehouse')    
            
                   
def handle_not_enough_items(item, sell_item_name, sell_item_quantity):
    flash(f'We dont have {sell_item_quantity} {item.unit} of {item.name}')   
    logging.info(f"We dont have {sell_item_quantity} of {sell_item_name}")
        
      
def calculate_value_of_products_in_stock(items):
    value = [float(item.unit_price) * float(item.quantity_in_stock) for item in items]
    return sum(value)
     
     
def calculate_value_of_sold_products(items):
    value = [float(item.unit_price) * float(item.quantity_sold) for item in items]
    return sum(value)
     
        
def remove_empty_items_from_db():            
    empty_items = Item.query.filter(Item.quantity_in_stock <= 0, Item.quantity_sold <= 0).all()
    for item in empty_items:
        db.session.delete(item)
    db.session.commit()
    logging.info(f"Database cleaned empty items.")