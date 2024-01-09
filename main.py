import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename="warehouse_manager.log")


items = [
    {
        'name': 'apple', 
        'quantity': 123, 
        'unit': 'kg', 
        'unit_price': 12.99,
        },
    {
        'name': 'tomato', 
        'quantity': 56, 
        'unit': 'kg', 
        'unit_price': 8.99,
        },
    {
        'name': 'oragne', 
        'quantity': 28, 
        'unit': 'kg', 
        'unit_price': 72.99,
        },
    {
        'name': 'kiwi', 
        'quantity': 3, 
        'unit': 'kg', 
        'unit_price': 26.99,
        },
    ]


def main():
    print_info()
    while True:
        user_decision = get_user_input("What would you like to do? exit/show/add/sell: ")  
        logging.info(f"User decision {user_decision}")
        if user_decision == 'exit':
            exit_program()
        elif user_decision == 'show':
            show_items()
        elif user_decision == 'add':
            add_items()
        elif user_decision == 'sell':
            sell_items()


def print_info():
    """Prints simple info."""
    logging.info("Start program warehouse_manager.py")
    print("--- warehouse_manager.py ---")
    
    
def get_user_input(question):
    """Get input string from user and returns lower and stripped."""
    user_input_string = input(question)
    logging.info(f"User input string: {user_input_string}")
    return user_input_string.lower().strip() if isinstance(user_input_string, str) else int(user_input_string)


def show_items():
    print("Name\t\tQuantity\tUnit\t\tPrice (PLN)\n"
          "----\t\t--------\t----\t\t-----------")
    for item in items:
        print(f"{item['name'].title()}\t\t{item['quantity']}\t\t{item['unit']}\t\t{item['unit_price']}")
        
        
def add_items():
    print("Adding to warehouse...")
    new_item = {
        'name': get_user_input("New item name: "), 
        'quantity': get_user_input("New item quantity: "), 
        'unit': get_user_input("New item unit: "), 
        'unit_price': get_user_input("New item unit price: "),
    }
    logging.info(f"New item to add: {new_item}")
    items.append(new_item)
    logging.info("New item added")
    
    
def sell_items():
    print("Sell from warehouse...")
    sell_item_name = get_user_input("Item to sell: ")
    sell_item_quantity = int(get_user_input(f"{sell_item_name} sell quantity: "))
    logging.info(f"Item to sell: {sell_item_name} quantity {sell_item_quantity}")
    for item in items:
        if item['name'] == sell_item_name:
            if item['quantity'] >= sell_item_quantity:
                item['quantity'] = item['quantity'] - sell_item_quantity
                print(f"Sold {sell_item_quantity} of {sell_item_name}")
                logging.info("Item sold")
                break
            else:
                print(f"We dont have {sell_item_quantity} of {sell_item_name}")
                logging.info(f"We dont have {sell_item_quantity} of {sell_item_name}")
                break
        else: 
            print(f"{sell_item_name} not found in warehouse")
            logging.info(f"{sell_item_name} not found in warehouse")


def exit_program():
    print("Exit program... Bye.")
    logging.info("Exit program warehouse_manager.py")
    exit(1)


if __name__ == "__main__":
    main()