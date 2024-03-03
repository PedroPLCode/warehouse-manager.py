from flask import Flask, render_template, abort, request, flash
from forms import ProductAddForm, ProductSaleForm
from utils import *
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log")

app = Flask(__name__)
app.secret_key = b'my-secret'

@app.route('/', methods=["GET"])
def show_base_view():
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )
    

@app.route('/load', methods=["GET"])
def load_data():
    pass
    flash('Data loaded succesfully.')  
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )
    

@app.route('/save', methods=["GET"])
def save_data():
    pass
    flash('Data saved succesfully.')  
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )

    
@app.route('/products', methods=["GET", "POST"])
def products_list():
    items = load_array_from_csv_file(file_warehouse)
    addItemForm = ProductAddForm()
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
    addItemForm = ProductAddForm()
    sellItemForm = ProductSaleForm()
    if product_name.strip() in items.keys():
        if request.method == 'GET':
            return render_template("sell_product.html", 
                                   date_and_time=get_current_time_and_date(), 
                                   form=sellItemForm, 
                                   product_name=product_name)
        elif request.method == 'POST':
            quantity_to_sell = request.form['quantity_to_sell']
            sell_items_from_warehouse(product_name, float(quantity_to_sell))
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

if __name__ == '__main__':
    app.run(debug=True)