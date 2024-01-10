import csv
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename="warehouse_manager.log")

items = []
sold_items = []

def main():
    print_info()
    load()
    while True:
        user_decision = get_user_input("What would you like to do? exit/show/add/sell/revenue/save/load: ")  
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
            save()
        elif user_decision == 'load':
            load()
        else:
            wrong_input()


def print_info():
    """Prints simple info."""
    logging.info("Start program warehouse_manager.py")
    print("--- warehouse_manager.py ---")
    
    
def get_user_input(question):
    """Get input string from user and returns lower and stripped."""
    user_input_string = input(question)
    logging.info(f"User input string: {user_input_string}")
    return user_input_string.lower().strip() if isinstance(user_input_string, str) else int(user_input_string)


def wrong_input():
    print("Wrong input. Try again.")
    logging.info("Wrong input.")
    

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
    new_item = create_item(get_user_input("New item name: "),
                         int(get_user_input("New item quantity: ")), 
                         get_user_input("New item unit: "),
                         int(get_user_input("New item unit price: "))
                         )
    logging.info(f"New item to add: {new_item}")
    items.append(new_item)
    logging.info("New item added")
    
    
def sell_items():
    print("Sell from warehouse...")
    sell_item_name = get_user_input("Item to sell: ")
    sell_item_quantity = int(get_user_input("Quantity to sell: "))
    logging.info(f"Item to sell: {sell_item_name} quantity {sell_item_quantity}")
    for item in items:
        if item['name'] == sell_item_name:
            if item['quantity'] >= sell_item_quantity:
                item['quantity'] = item['quantity'] - sell_item_quantity
                print(f"Succesfully sold {sell_item_quantity} {item['unit']} of {sell_item_name}")
                sold_item = create_item(sell_item_name,
                                      sell_item_quantity,
                                      item['unit'],
                                      item['unit_price'])
                sold_items.append(sold_item)
                logging.info("Item sold")
                break
            else:
                print(f"We dont have {sell_item_quantity} {item['unit']} of {sell_item_name}s")
                logging.info(f"We dont have {sell_item_quantity} of {sell_item_name}")
                break
        else: 
            print(f"{sell_item_name} not found in warehouse")
            logging.info(f"{sell_item_name} not found in warehouse")


def calculate_value_of_products(array):
    value = [item['unit_price'] * item['quantity'] for item in array]
    return sum(value)


def show_revenue():
    income = calculate_value_of_products(sold_items)
    costs = calculate_value_of_products(items)
    print("Revenue breakdown (PLN)"
          f"Income: {income}\n"
          f"Costs: {costs}\n"
          "-----------------------"
          f"Revenue: {income - costs}")


def export_items_to_csv(array, filename):
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
    
def save():
    export_items_to_csv(items, 'warehouse.csv')
    export_items_to_csv(sold_items, 'sold.csv')
    
    
def load_items_from_csv(array, filename):
    array.clear()
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
            
            
def load():
    load_items_from_csv(items, 'warehouse.csv')
    load_items_from_csv(sold_items, 'sold.csv')
    
    
def exit_program():
    print("Exit program... Bye.")
    logging.info("Exit program warehouse_manager.py")
    save()
    exit(1)


if __name__ == "__main__":
    main()