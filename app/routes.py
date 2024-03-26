from flask import abort, render_template, url_for, request, redirect, flash
from app.utils import *
from app import app, db
from app.models import Item
from app.forms import ProductAddForm, ProductSaleForm
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename="warehouse_manager.log"
                    )

app.secret_key = b'my-super-secret-key'
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
    
    addItemForm = ProductAddForm()
    
    if request.method == "POST":
        if not request.form:
            abort(400)
        if not addItemForm.validate_on_submit():
            items = Item.query.all()
            new_item = create_new_product_instance(request.form['name'],
                                          request.form['quantity_in_stock'],
                                          0,
                                          request.form['unit'],
                                          request.form['unit_price'],
                                          )
            if item_already_in_db(new_item, items):
                update_existing_item(new_item, items)
            else:      
                add_new_item_to_db(new_item)
                
    search_query = request.args.get('search')
    if search_query:
        items = Item.query.filter(Item.name.ilike(f"%{search_query}%"), 
                                  Item.quantity_in_stock > 0).all()
        items_found_count = len(items)
        items_count = len(Item.query.filter(Item.quantity_in_stock > 0).all())
    else:
        items = Item.query.filter(Item.quantity_in_stock > 0).all()
        items_count = len(items)
        items_found_count = None
        
    sorted_items = sorted([item if item.quantity_in_stock > 0 else None for item in items], 
                          key=lambda item: item.id)
    return render_template("products_list.html", 
                           date_and_time=get_current_time_and_date(), 
                           form=addItemForm, 
                           items=sorted_items,
                           items_found_count=items_found_count,
                           items_count=items_count,
                           search_query=search_query if search_query else None,
                           )
    
    
@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product(product_name):
    items = Item.query.all()
    addItemForm = ProductAddForm()
    sellItemForm = ProductSaleForm()
    
    if item_found_in_db(product_name, items):
        if request.method == 'GET':
            return render_template("sell_product.html", 
                                   date_and_time=get_current_time_and_date(), 
                                   form=sellItemForm, 
                                   product_name=product_name)
        elif request.method == 'POST':
            quantity_to_sell = request.form['quantity_to_sell']
            sell_items_from_warehouse(product_name, float(quantity_to_sell), items)
            remove_empty_items_from_db()
            return redirect(url_for("products_list"))


@app.route('/sold', methods=["GET",])
def sold_list():
    global prev_path 
    prev_path = request.path
    
    search_query = request.args.get('search')
    if search_query:
        items = Item.query.filter(Item.name.ilike(f"%{search_query}%"), 
                                  Item.quantity_sold > 0).all()
        items_found_count = len(items)
        items_count = len(Item.query.filter(Item.quantity_sold > 0).all())
    else:
        items = Item.query.filter(Item.quantity_sold > 0).all()
        items_count = len(items)
        items_found_count = None
    
    sorted_items = sorted([item if item.quantity_in_stock > 0 else None for item in items], 
                          key=lambda item: item.id)
    return render_template('sold_items_list.html', 
                           date_and_time=get_current_time_and_date(), 
                           items=sorted_items,
                           items_found_count=items_found_count,
                           items_count=items_count,
                           search_query=search_query if search_query else None
                           )


@app.route('/remove/<product_name>', methods=["POST"])
def remove_sold_item(product_name):
    item = Item.query.filter(Item.name == product_name).first()
    if item.quantity_in_stock > 0:
        item.quantity_sold = 0
        db.session.add(item)
    else:
        db.session.delete(item)
    db.session.commit()
    flash(f'{product_name} succesfully removed from list.')
    remove_empty_items_from_db()
    
    return redirect(url_for("sold_list"))
    

@app.route('/revenue', methods=["GET"])
def show_revenue():
    global prev_path 
    prev_path = request.path
    items = Item.query.all()
    income = calculate_value_of_sold_products(items) if items else 0
    costs = calculate_value_of_products_in_stock(items) if items else 0
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