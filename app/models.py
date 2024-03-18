from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    quantity_in_stock = db.Column(db.Integer, index=True)
    quantity_sold = db.Column(db.Integer, index=True)
    unit = db.Column(db.String(100), index=True)
    unit_price = db.Column(db.Integer, index=True)

    def __str__(self):
        return (f"Item:\nname: {self.name}"
                f"\nquantity_in_stock: {self.quantity_in_stock}"
                f"\nquantity_sold: {self.quantity_sold}"
                f"\nunit: {self.unit}" 
                f"\nunit_price: {self.unit_price}")