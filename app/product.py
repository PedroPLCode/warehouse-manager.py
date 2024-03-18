class Product:
    
    def __init__(self, name, quantity_in_stock, quantity_sold, unit, unit_price, product_index):
        self.name = name
        self.quantity_in_stock = quantity_in_stock
        self.quantity_sold = quantity_sold
        self.unit = unit
        self.unit_price = unit_price
        self.product_index = product_index
       
    def __str__(self):
        return (f"{self.name.title()}\t\t{self.quantity}\t\t{self.unit}\t\t{self.unit_price}\t\t{self.product_index}")
       
    def __repr__(self):
        return (f"Name: {self.name.title()}\n"
                f"Quantity in stock: {self.quantity_in_stock}\n"
                f"Quantity sold: {self.quantity_sold}\n"
                f"Unit: {self.unit}\n"
                f"Unit price: {self.unit_price}\n"
                f"Product index {self.product_index}\n")
        
    def __eq__(self, other):
        return (self.name).strip().lower() == (other.name).strip().lower()