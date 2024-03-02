from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    unit_price = DecimalField('Unit price', validators=[DataRequired()])
    
class ProductSaleForm(FlaskForm):
    quantity_to_sell = IntegerField('Quantity to sell', validators=[DataRequired()])