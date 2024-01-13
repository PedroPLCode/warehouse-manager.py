"""Warehouse manager
Author: Pedro van Code
Last update: 10.01.2024
Any comments welcome :)
"""

import sys
import csv
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log")

items = []
sold_items = []

def main(file_warehouse, file_sold_items):
    print_info()
    load(file_warehouse, file_sold_items)
    while True:
        user_decision = get_user_input('str', "What would you like to do? exit/show/add/sell/revenue/save/load: ")  
        logging.info(f"User decision {user_decision}")
        if user_decision == 'exit':
            exit_program()
        elif user_decision == 'show':
            show_items()
        elif user_decision == 'add':
            add_items()
        elif user_decision == 'sell':
            sell_items()
        elif user_decision == 'revenue':
            show_revenue()
        elif user_decision == 'save':
            save(file_warehouse, file_sold_items)
        elif user_decision == 'load':
            load(file_warehouse, file_sold_items)
        else:
            wrong_input()


def print_info():
    """Prints simple info."""
    logging.info("Start program warehouse_manager.py")
    print("--- warehouse_manager.py ---")
    
    
def get_user_input(type, question):
    """Get input from user and returns lower and stripped if string or float if number."""
    while True:
        user_input = input(question)
        logging.info(f"User input: {user_input}")
        if type == 'str':
            if is_string(user_input):
                return user_input.lower().strip()
            else:
                print("Wrong input. Not a string. Try again.")
                logging.warning(f"{user_input} not a string.")
        elif type == 'num':
            if not is_string(user_input):
                return convert_input_to_float(user_input)
            else:
                print("Wrong input. Lookas like string. Try again.")
                logging.warning(f"{user_input} is a string.")


def wrong_input():
    print("Wrong input. Try again.")
    logging.warning("Wrong input.")
    

def show_items():
    print("Name\t\tQuantity\tUnit\t\tPrice (PLN)\n"
          "----\t\t--------\t----\t\t-----------")
    for item in items:
        print(f"{item['name'].title()}\t\t{item['quantity']}\t\t{item['unit']}\t\t{item['unit_price']}")  
        
        
def create_item(name, quantity, unit, unit_price):
    return {
        'name': name, 
        'quantity': quantity, 
        'unit': unit, 
        'unit_price': unit_price,
    }
    
        
def add_items():
    print("Adding to warehouse...")
    new_item = create_item(get_user_input('str', "New item name: "),
                           round(get_user_input('num', "New item quantity: "), 2),
                           get_user_input('str', "New item unit: "),
                           round(get_user_input('num', "New item unit price: "), 2)
                           )
    if item_already_in_array(new_item, items):
        update_existing_item(new_item, items)
    else:      
        create_new_item(new_item, items)
    

def update_existing_item(new_item, items):
    print(f"{new_item['name']} already exists in warehouse. Trying to update...")
    for item in items:
        if new_item['name'] == item['name']:
            if new_item['unit'] != item['unit']:
                print("Diffrent unit. Please add this product again with diffrent name.")
            elif new_item['unit_price'] != float(item['unit_price']):
                print("Diffrent unit price. Please add this product again with diffrent name.")
            else:
                item['quantity'] = float(item['quantity']) + float(new_item['quantity'])
                print(f"Succesfully added {new_item['quantity']} {item['unit']} {item['name']}s to warehouse.")
                export_array_to_csv(items, file_warehouse)
                logging.info(f"Added {new_item['quantity']} {item['unit']} {item['name']}s to warehouse.")
    
    
def create_new_item(new_item, items):
    items.append(new_item)
    print("Succesfully added new item to warehouse.")
    export_array_to_csv(items, file_warehouse)
    logging.info("New item added")
        
    
def item_already_in_array(new_item, array):  
    for item in array:
        if item['name'] == new_item['name']:
            return True

    
def convert_input_to_float(input):
    """Converts entered decimals with ',' to floats with '.' if possible."""
    if ',' in input:
        splitted = input.split(',')
        return float(splitted[0]+'.'+splitted[1]) if len(splitted) == 2 else input
    else:
        return float(input)
    
    
def is_string(input):
    """Checks if input is float (returns False), int (returns False) or string (returns True)."""
    try:
        input = float(convert_input_to_float(input))
        logging.info(f"{input} is float")
        return False
    except ValueError:
        try:
            input = int(input)
            logging.info(f"{input} is integer")
            return False
        except ValueError:
            logging.error(f"{input} is string")
            return True
        
    
def sell_items():
    print("Sell from warehouse...")
    sell_item_name = get_user_input('str', "Item to sell: ")
    sell_item_quantity = round(get_user_input('num', "Quantity to sell: "), 2)
    logging.info(f"Item to sell: {sell_item_name} quantity {sell_item_quantity}")
    item_found = False
    for item in items:
        if item['name'] == sell_item_name:
            if float(item['quantity']) >= sell_item_quantity:
                sell_action(item, sell_item_name, sell_item_quantity)
                save(file_warehouse, file_sold_items)
                item_found = True
                break
            else:
                not_enough_items(item, sell_item_name, sell_item_quantity)
                item_found = True
                break
    if not item_found:
        item_not_found(sell_item_name)


def sell_action(item, sell_item_name, sell_item_quantity):
    item['quantity'] = round(float(item['quantity']) - sell_item_quantity, 2)
    sold_item = create_item(sell_item_name,
                            sell_item_quantity,
                            item['unit'],
                            item['unit_price'])
    sold_items.append(sold_item)
    print(f"Succesfully sold {sell_item_quantity} {item['unit']} of {sell_item_name}")
    logging.info("Item sold")
                   
                   
def not_enough_items(item, sell_item_name, sell_item_quantity):
    print(f"We dont have {sell_item_quantity} {item['unit']} of {sell_item_name}s")
    logging.info(f"We dont have {sell_item_quantity} of {sell_item_name}")


def item_not_found(item):
    print(f"{item} not found in warehouse")
    logging.info(f"{item} not found in warehouse")
    
    
def calculate_value_of_products(array):
    value = [float(item['unit_price']) * float(item['quantity']) for item in array]
    return sum(value)


def show_revenue():
    income = calculate_value_of_products(sold_items)
    costs = calculate_value_of_products(items)
    print("Revenue breakdown (PLN)\n"
          f"Income: {round(income, 2)}\n"
          f"Costs: {round(costs, 2)}\n"
          "-----------------------\n"
          f"Revenue: {round(income - costs, 2)}")
    
    
def remove_empty_items(array):
    for item in array:
        if float(item['quantity']) <= 0:
            array.remove(item)
            
     
def clear_arrays_from_empty_items(warehouse, sold_items):
    remove_empty_items(warehouse)
    remove_empty_items(sold_items)
    logging.info(f"Warehouse and Sold_items cleaned empty items.")


def export_array_to_csv(array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'quantity', 'unit', 'unit_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in array:
            writer.writerow({'name': item['name'],
                             'quantity': item['quantity'],
                             'unit': item['unit'],
                             'unit_price': item['unit_price']})
        print(f"Saved {filename}")
        logging.info(f"Saved {filename}")
    
    
def load_array_from_csv(array, filename):
    array.clear()
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_item = create_item(row['name'],
                                        row['quantity'],
                                        row['unit'],
                                        row['unit_price'])
                array.append(temp_item)
        print(f"Loaded {filename}")
        logging.info(f"Loaded {filename}")
    except FileNotFoundError:
        file_not_found(filename)
        
        
def file_not_found(filename):
    print(f"File {filename} not found")
    logging.info(f"File {filename} not found")
            

def save(file_warehouse, file_sold_items):
    clear_arrays_from_empty_items(items, sold_items)
    export_array_to_csv(items, file_warehouse)
    export_array_to_csv(sold_items, file_sold_items)
    
            
def load(file_warehouse, file_sold_items):
    load_array_from_csv(items, file_warehouse)
    load_array_from_csv(sold_items, file_sold_items)
    clear_arrays_from_empty_items(items, sold_items)
    
    
def exit_program():
    print("Exit program... Bye.")
    logging.info("Exit program warehouse_manager.py")
    save(file_warehouse, file_sold_items)
    exit(1)
    
    
def program_not_start():
    print("Program cant start without necessary arguments.\n"
          "Try python3 warehouse_manager.py file_warehouse.csv file_sold_items.csv")
    logging.info("Didnt start. Missing required argunemts / filemanes")
    exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        file_warehouse = sys.argv[1]
        file_sold_items = sys.argv[2]
        main(file_warehouse, file_sold_items)
    else:
        print_info()
        program_not_start()