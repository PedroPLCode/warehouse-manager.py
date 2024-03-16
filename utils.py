from flask import flash
from product import Product
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


def sell_items_from_warehouse(sell_item_name, sell_item_quantity):
    items = load_dict_from_csv_file(file_warehouse)
    logging.info(f"Item to sell: {sell_item_name} quantity {sell_item_quantity}")
    for item in items.values():
        if (item.name).strip().lower() == sell_item_name.strip().lower():
            if float(item.quantity) >= sell_item_quantity:
                sell_action(item, sell_item_name, sell_item_quantity)
                break
            else:
                handle_not_enough_items(item, sell_item_name, sell_item_quantity)
                break


def sell_action(item, sell_item_name, sell_item_quantity):
    items = load_dict_from_csv_file(file_warehouse)
    sold_items = load_dict_from_csv_file(file_sold_items)
    if not sold_items:
        sold_items = {}
    item.quantity = round(float(item.quantity) - sell_item_quantity, 2)
    items[item.name].quantity = item.quantity
    sold_item = create_new_product(sell_item_name,
                                sell_item_quantity,
                                item.unit,
                                item.unit_price,
                                len(sold_items) if sold_items else 1,
                                )
    sold_items[sold_item.name] = sold_item
    logging.info(f"Item {sell_item_name} sold")     
    flash(f'{sold_item.quantity} {sold_item.unit} {sold_item.name} '
          f'succesfully sold from warehouse')    
    export_dict_to_csv_file(items, file_warehouse)
    export_dict_to_csv_file(sold_items, file_sold_items)
            
                   
def handle_not_enough_items(item, sell_item_name, sell_item_quantity):
    flash(f'We dont have {sell_item_quantity} {item.unit} of {item.name}')   
    logging.info(f"We dont have {sell_item_quantity} of {sell_item_name}")
        
    
def create_new_product(name, quantity, unit, unit_price, product_index):
    return Product(name, quantity, unit, unit_price, product_index)
    
    
def update_existing_item(new_item, items):
    for item in items.values():
        if items_match(item, new_item):
            if not item_in_conflict_with_other_items(new_item, item):
                update_item_action(item, new_item)
                export_dict_to_csv_file(items, file_warehouse)
                logging.info(f"Added {new_item.quantity} "
                             f"{item.unit} {item.name} to warehouse.")
                 
                              
def update_item_action(item, new_item):
    item.quantity = float(item.quantity) + float(new_item.quantity)
    flash(f'Added {new_item.quantity} {new_item.unit} '
          f'of {new_item.name} to warehouse.')
              
              
def items_match(item_one, item_two):
    return True if item_one == item_two else False
   
   
def item_in_conflict_with_other_items(item_one, item_two):
    if item_one.unit != item_two.unit or item_one.unit_price != item_two.unit_price:
        flash(f'Diffrent unit or unit price. '
              f'Try add this product with diffrent name.')   
        return True
    else:
        return False
    
    
def add_new_item_to_warehouse(new_item, items):
    items[new_item.name] = new_item
    export_dict_to_csv_file(items, file_warehouse)
    flash(f'{new_item.quantity} {new_item.unit} {new_item.name} '
          f'succesfully added to warehouse')
    logging.info("New item added")
    
    
def item_already_in_dict(item, dict):  
    if not dict: 
        return False
    for item_from_dict in dict.values():
        if items_match(item_from_dict, item):
            return True
    return False
      
      
def calculate_value_of_products(array):
    value = [float(item.unit_price) * float(item.quantity) for item in array]
    return sum(value)
     
     
def load_dict_from_csv_file(filename):
    dict = {}
    product_index = 1
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_item = create_new_product(row['name'], 
                                               row['quantity'], 
                                               row['unit'], 
                                               row['unit_price'], 
                                               product_index
                                               )
                dict[temp_item.name] = temp_item
                product_index += 1
        logging.info(f"Loaded {filename}")
        remove_empty_items_from_dict(dict)
        return dict
    except FileNotFoundError:
        handle_file_not_found(filename)
        

def handle_file_not_found(filename):
    logging.info(f"File {filename} not found")     
     
     
def export_dict_to_csv_file(dict, filename):
    remove_empty_items_from_dict(dict)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'quantity', 'unit', 'unit_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in dict.values():
            writer.writerow({'name': item.name,
                             'quantity': item.quantity,
                             'unit': item.unit,
                             'unit_price': item.unit_price}
                            )
        logging.info(f"Saved {filename}")
        
        
def remove_empty_items_from_dict(dict):            
    keys_to_delete = [] 
    for key, item in dict.items(): 
        if float(item.quantity) <= 0:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del dict[key]
    logging.info(f"{dict} cleaned empty items.")