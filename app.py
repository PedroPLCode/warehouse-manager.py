from flask import Flask, render_template, url_for, request, redirect, flash
from product import Product
from forms import ProductForm
import datetime
import os
import sys
import csv
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log")

app = Flask(__name__)

file_warehouse = './warehouse.csv'
file_sold_items = './sold.csv'
items = []
sold_items = []

@app.route('/', methods=["GET"])
def show_base_view():
    return render_template('homepage.html')


@app.route('/products', methods=["GET"])
def show_products_list():
    items = load_array_from_csv_file(file_warehouse)
    remove_empty_items_from_array(items)
    return render_template('products_list.html', items=items)


@app.route('/products', methods=["POST"])
def add_new_item_to_items_array():
    form = ProductForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            new_item = create_new_product(request.json.get('description', ""),
                                        request.json.get('quantity', ""),
                                        request.json.get('price', ""),
                                        request.json.get('unit_price', ""),
                                        )
            if item_already_in_array(new_item, items):
                update_existing_item(new_item, items)
            else:      
                add_new_item_to_warehouse(new_item, items)
            return redirect(url_for("products_list"))
    return render_template("products_list.html", form=form, error=error)


@app.route('/sold')
def show_sold_list():
    sold_items = load_array_from_csv_file(file_sold_items)
    remove_empty_items_from_array(sold_items)
    return render_template('sold_items_list.html', sold_items=sold_items)


# IS NEEDED ???
def load_data_from_files(file_warehouse, file_sold_items):
    items = load_array_from_csv_file(file_warehouse)
    sold_items = load_array_from_csv_file(file_sold_items)
    remove_empty_items_from_array(items)
    remove_empty_items_from_array(sold_items)
    

def load_array_from_csv_file(filename):
    #array.clear()
    array = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_item = create_new_product(row['name'], row['quantity'], row['unit'], row['unit_price'])
                array.append(temp_item)
        logging.info(f"Loaded {filename}")
        return array
    except FileNotFoundError:
        handle_file_not_found(filename)
        
        
def handle_file_not_found(filename):
    logging.info(f"File {filename} not found")     
        
    
def remove_empty_items_from_array(array):
    for item in array:
        if float(item.quantity) <= 0:
            array.remove(item)
    logging.info(f"{array} cleaned empty items.")
    
    
def create_new_product(name, quantity, unit, unit_price):
    return Product(name, quantity, unit, unit_price)
    
    
def update_existing_item(new_item, items):
    print(f"{new_item.name} already exists in warehouse. Trying to update...")
    for item in items:
        if items_match(item, new_item):
            if not item_in_conflict_with_other_items(new_item, item):
                update_item_action(item, new_item)
                print(f"Succesfully added {new_item.quantity} {item.unit} {item.name}s to warehouse.")
                export_array_to_csv_file(items, file_warehouse)
                logging.info(f"Added {new_item.quantity} {item.unit} {item.name}s to warehouse.")
                 
                              
def update_item_action(item, new_item):
    item.quantity = float(item.quantity) + float(new_item.quantity)
              
              
def items_match(item_one, item_two):
    return True if item_one == item_two else False
   
   
def item_in_conflict_with_other_items(item_one, item_two):
    if item_one.unit != item_two.unit or item_one.unit_price != float(item_two.unit_price):
        print("Diffrent unit or unit price. Please add this product again with diffrent name.")
        return True
    else:
        return False
    
    
def add_new_item_to_warehouse(new_item, items):
    items.append(new_item)
    print("Succesfully added new item to warehouse.")
    export_array_to_csv_file(items, file_warehouse)
    logging.info("New item added")
    
    
def item_already_in_array(item, array):  
    for item_from_array in array:
        if items_match(item_from_array, item):
            return True
    
    
# OLD FUNCTIONS TO SORT / REFACTOR !!!
def main(file_warehouse, file_sold_items):
    load_data(file_warehouse, file_sold_items)
    if user_decision == 'exit':
        pass
    elif user_decision == 'help':
        pass
    elif user_decision == 'show':
        pass
    elif user_decision == 'add':
        add_items_to_warehouse()
    elif user_decision == 'sell':
        sell_items_from_warehouse()
    elif user_decision == 'revenue':
        show_revenue()
    elif user_decision == 'save':
        save_data(file_warehouse, file_sold_items)
    elif user_decision == 'load':
        load_data(file_warehouse, file_sold_items)
    else:
        handle_wrong_input()

    
def get_user_input(type, question):
    while True:
        user_input = input(question)
        logging.info(f"User input: {user_input}")
        if type == 'str':
            if is_string(user_input):
                return user_input.lower().strip()
            else:
                print("Wrong input. Not a string. Try again.")
                logging.warning(f"{input} not a string.")
        elif type == 'num':
            if not is_string(user_input):
                return convert_input_to_float(user_input)
            else:
                print("Wrong input. Lookas like string. Try again.")
                logging.warning(f"{input} is a string.")


def handle_wrong_input():
    print("Wrong input. Try again.")
    logging.warning("Wrong input.")
              
    
def convert_input_to_float(input):
    if ',' in input:
        splitted = input.split(',')
        return float(splitted[0]+'.'+splitted[1]) if len(splitted) == 2 else input
    else:
        return float(input)  
    
    
def is_string(input):
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
            logging.info(f"{input} is string")
            return True       
    
    
def sell_items_from_warehouse():
    print("\nSell from warehouse...")
    sell_item_name = get_user_input('str', "Item to sell: ")
    sell_item_quantity = round(get_user_input('num', "Quantity to sell: "), 2)
    logging.info(f"Item to sell: {sell_item_name} quantity {sell_item_quantity}")
    item_found = False
    for item in items:
        if (item.name).strip().lower() == sell_item_name.strip().lower():
            if float(item.quantity) >= sell_item_quantity:
                sell_action(item, sell_item_name, sell_item_quantity)
                save_data(file_warehouse, file_sold_items)
                item_found = True
                break
            else:
                handle_not_enough_items(item, sell_item_name, sell_item_quantity)
                item_found = True
                break
    if not item_found:
        handle_item_not_found(sell_item_name)


def sell_action(item, sell_item_name, sell_item_quantity):
    item.quantity = round(float(item.quantity) - sell_item_quantity, 2)
    sold_item = create_new_product(sell_item_name,
                            sell_item_quantity,
                            item.unit,
                            item.unit_price)
    sold_items.append(sold_item)
    print(f"Succesfully sold {sell_item_quantity} {item.unit} of {sell_item_name}")
    logging.info("Item sold")         
            
                   
def handle_not_enough_items(item, sell_item_name, sell_item_quantity):
    print(f"We dont have {sell_item_quantity} {item.unit} of {sell_item_name}s")
    logging.info(f"We dont have {sell_item_quantity} of {sell_item_name}")


def handle_item_not_found(item):
    print(f"{item} not found in warehouse")
    logging.info(f"{item} not found in warehouse")
      
      
def calculate_value_of_products(array):
    value = [float(item.unit_price) * float(item.quantity) for item in array]
    return sum(value)


def show_revenue():
    income = calculate_value_of_products(sold_items)
    costs = calculate_value_of_products(items)
    print("\nRevenue breakdown (PLN)\n"
          f"Income: {round(income, 2)}\n"
          f"Costs: {round(costs, 2)}\n"
          "-----------------------\n"
          f"Revenue: {round(income - costs, 2)}")
     
     
def export_array_to_csv_file(array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'quantity', 'unit', 'unit_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in array:
            writer.writerow({'name': item.name,
                             'quantity': item.quantity,
                             'unit': item.unit,
                             'unit_price': item.unit_price})
        print(f"Saved {filename}")
        logging.info(f"Saved {filename}")


def save_data(file_warehouse, file_sold_items):
    clear_warehouse_from_empty_items(items, sold_items)
    export_array_to_csv_file(items, file_warehouse)
    export_array_to_csv_file(sold_items, file_sold_items)
     
     
def exit_program():
    save_data(file_warehouse, file_sold_items)
    print("\nExit program... Bye.\n")
    logging.info("Exit program warehouse_manager.py")
    exit(1)
    
    
def program_not_start():
    print("Program cant start without necessary arguments.\n"
          "Try python3 warehouse_manager.py file_warehouse.csv file_sold_items.csv")
    logging.info("Didnt start. Missing required argunemts / filemanes")
    exit(1)

        
if __name__ == '__main__':
    app.run(debug=True)