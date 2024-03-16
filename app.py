from flask import Flask, render_template, abort, request, flash, redirect, url_for
from forms import ProductAddForm, ProductSaleForm
from utils import *
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log"
                    )

app = Flask(__name__)
app.secret_key = b'my-secret-key'
prev_path = ''

@app.errorhandler(404)
def handle_page_not_found(error):
    return redirect(url_for("show_base_view"))


@app.route('/', methods=["GET"])
def show_base_view():
    global prev_path
    prev_path = request.path
    return render_template('homepage.html', 
                           date_and_time=get_current_time_and_date()
                           )

    
@app.route('/products', methods=["GET", "POST"])
def products_list():
    global prev_path 
    prev_path = request.path
    search_query = request.args.get('search')
    items = load_dict_from_csv_file(file_warehouse)
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
                
    if search_query:
        items = [item for item in items.values() if search_query in item.name]
    else:
        items = items.values()
        
    return render_template("products_list.html", 
                           date_and_time=get_current_time_and_date(), 
                           form=addItemForm, 
                           items=items if items else {},
                           search_query=search_query if search_query else None
                           )
    
    
@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product(product_name):
    items = load_dict_from_csv_file(file_warehouse)
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
            items = load_dict_from_csv_file(file_warehouse)
            return render_template("products_list.html", 
                                    date_and_time=get_current_time_and_date(), 
                                    items=items.values() if items else {}, 
                                    form=addItemForm, 
                                    )


@app.route('/sold', methods=["GET",])
def sold_list():
    global prev_path 
    prev_path = request.path
    search_query = request.args.get('search')
    sold_items = load_dict_from_csv_file(file_sold_items)
    
    if search_query:
        sold_items = [item for item in sold_items.values() if search_query in item.name]
    else:
        sold_items = sold_items.values()
        
    return render_template('sold_items_list.html', 
                           date_and_time=get_current_time_and_date(), 
                           items=sold_items if sold_items else {},
                           search_query=search_query if search_query else None
                           )


@app.route('/remove/<product_name>', methods=["POST"])
def remove_sold_item(product_name):
    sold_items = load_dict_from_csv_file(file_sold_items)    
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
    

@app.route('/revenue', methods=["GET"])
def show_revenue():
    global prev_path 
    prev_path = request.path
    items = load_dict_from_csv_file(file_warehouse)
    sold_items = load_dict_from_csv_file(file_sold_items)
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
    
    
@app.route('/load', methods=["GET"])
def load_data():
    pass
    flash('CSV data loaded succesfully.')
    if prev_path == '/products':
        return redirect(url_for("products_list"))
    elif prev_path == '/sold':
        return redirect(url_for("sold_list"))
    elif prev_path == '/revenue':
        return redirect(url_for("show_revenue"))  
    else: 
        return redirect(url_for("show_base_view"))  
    

@app.route('/save', methods=["GET"])
def save_data():
    pass
    flash('CSV data saved succesfully.')
    if prev_path == '/products':
        return redirect(url_for("products_list"))
    elif prev_path == '/sold':
        return redirect(url_for("sold_list"))
    elif prev_path == '/revenue':
        return redirect(url_for("show_revenue"))  
    else: 
        return redirect(url_for("show_base_view"))  

if __name__ == '__main__':
    app.run(debug=True)