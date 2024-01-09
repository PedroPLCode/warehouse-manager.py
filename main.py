import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename="warehouse_manager.log")

def main():
    logging.info("Start program warehouse_manager.py")
    print_info()
    while True:
        user_input = get_user_input()  
        if user_input == 'exit' or user_input == 'e':
            exit_program()

def print_info():
    """Prints simple info."""
    print("--- warehouse_manager.py ---")
    
def get_user_input():
    """Get input string from user and returns lower and stripped."""
    user_input_string = input("What would you like to do? ")
    logging.info(f"User input string: {user_input_string}")
    return user_input_string.lower().strip()

def exit_program():
    print("Exiting... Bye.")
    logging.info("Exit program warehouse_manager.py")
    exit(1)

if __name__ == "__main__":
    main()