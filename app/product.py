class Product:
    
    def __init__(self, name, quantity_in_stock, quantity_sold, unit, unit_price):
        self.name = name
        self.quantity_in_stock = quantity_in_stock
        self.quantity_sold = quantity_sold
        self.unit = unit
        self.unit_price = unit_price
       
    def __str__(self):
        return (f"{self.name.title()}\t\t{self.quantity}\t\t{self.unit}\t\t{self.unit_price}")
       
    def __repr__(self):
        return (f"Name: {self.name.title()}\n"
                f"Quantity in stock: {self.quantity_in_stock}\n"
                f"Quantity sold: {self.quantity_sold}\n"
                f"Unit: {self.unit}\n"
                f"Unit price: {self.unit_price}\n")
        
    def __eq__(self, other):
        return (self.name).strip().lower() == (other.name).strip().lower()