# słownik zamiast listy
# szybkie wyszukiwanie
# jednostki int float
# reafaktoryzacja całości

from flask import Flask, render_template, abort, request, flash
from product import Product
from forms import ProductForm, ProductSaleForm
import datetime
import csv
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log")

app = Flask(__name__)
app.secret_key = b'my-secret'

file_warehouse = './warehouse.csv'
file_sold_items = './sold.csv'

@app.route('/', methods=["GET"])
def show_base_view():
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )
    

@app.route('/load', methods=["GET"])
def load_data():
    flash('Data loaded succesfully')  
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )
    

@app.route('/save', methods=["GET"])
def save_data():
    flash('Data saved succesfully')  
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )

    
@app.route('/products', methods=["GET", "POST"])
def products_list():
    items = load_array_from_csv_file(file_warehouse)
    addItemForm = ProductForm()
    if request.method == "POST":
        if not request.form:
            abort(400)
        if not addItemForm.validate_on_submit():
            new_item = create_new_product(request.form['name'],
                                          request.form['quantity'],
                                          request.form['unit'],
                                          request.form['unit_price'],
                                          len(items) if items else 1,
                                          )
            if item_already_in_dict(new_item, items):
                update_existing_item(new_item, items)
            else:      
                add_new_item_to_warehouse(new_item, items if items else {})
    return render_template("products_list.html", 
                           date_and_time=get_current_time_and_date(), 
                           form=addItemForm, 
                           items=items.values() if items else {}
                           )


@app.route('/sold', methods=["GET",])
def sold_list():
    sold_items = load_array_from_csv_file(file_sold_items)
    return render_template('sold_items_list.html', 
                           date_and_time=get_current_time_and_date(), 
                           items=sold_items.values() if sold_items else {}
                           )


@app.route('/remove/<product_name>', methods=["POST"])
def remove_sold_item(product_name):
    sold_items = load_array_from_csv_file(file_sold_items)    
    keys_to_delete = []
    for single_key in sold_items.keys():
        if single_key.strip() == product_name.strip():
            keys_to_delete.append(single_key)
    for key in keys_to_delete:
        del sold_items[key]
    export_dict_to_csv_file(sold_items, file_sold_items)
    flash(f'{single_key} succesfully removed from list.')
    return render_template('sold_items_list.html', 
                           date_and_time=get_current_time_and_date(), 
                           items=sold_items.values()
                           )


@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product(product_name):
    items = load_array_from_csv_file(file_warehouse)
    addItemForm = ProductForm()
    sellItemForm = ProductSaleForm()
    if product_name.strip() in items.keys():
        if request.method == 'GET':
            return render_template("sell_product.html", 
                                   date_and_time=get_current_time_and_date(), 
                                   form=sellItemForm, 
                                   product_name=product_name)
        elif request.method == 'POST':
            quantity_to_sell = request.form['quantity_to_sell']
            sell_items_from_warehouse(product_name, int(quantity_to_sell))
    items = load_array_from_csv_file(file_warehouse)
    return render_template("products_list.html", 
                           date_and_time=get_current_time_and_date(), 
                           items=items.values() if items else {}, 
                           form=addItemForm, 
                           )
    

@app.route('/revenue', methods=["GET"])
def show_revenue():
    items = load_array_from_csv_file(file_warehouse)
    sold_items = load_array_from_csv_file(file_sold_items)
    income = calculate_value_of_products(sold_items.values()) if sold_items else 0
    costs = calculate_value_of_products(items.values()) if sold_items else 0
    total = income - costs
    revenue = [
        {
          'text': 'Income',
          'value': round(income, 2),
        },
        {
          'text': 'Costs',
          'value': round(costs, 2),
        },
        {
          'text': 'Revenue',
          'value': round(total, 2),
        }
    ]
    return render_template('revenue.html', 
                           date_and_time=get_current_time_and_date(), 
                           revenue=revenue)


def get_current_time_and_date():
    date_and_time = datetime.datetime.now()
    return date_and_time.strftime("%X %x")


def sell_items_from_warehouse(sell_item_name, sell_item_quantity):
    items = load_array_from_csv_file(file_warehouse)
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
    items = load_array_from_csv_file(file_warehouse)
    sold_items = load_array_from_csv_file(file_sold_items)
    if not sold_items:
        sold_items = {}
    item.quantity = round(int(item.quantity) - sell_item_quantity, 2)
    items[item.name].quantity = item.quantity
    sold_item = create_new_product(sell_item_name,
                            sell_item_quantity,
                            item.unit,
                            item.unit_price,
                            len(sold_items) if sold_items else 1,
                            )
    sold_items[sold_item.name] = sold_item
    logging.info("Item sold")     
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
     
     
def load_array_from_csv_file(filename):
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


if __name__ == '__main__':
    app.run(debug=True)