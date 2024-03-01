from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    unit_price = DecimalField('Unit prive', validators=[DataRequired()])