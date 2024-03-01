from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Tytuł', validators=[DataRequired()])
    quantity = DecimalField('Opis', validators=[DataRequired()])
    unit = DecimalField('Opis', validators=[DataRequired()])
    unit_price = DecimalField('Opis', validators=[DataRequired()])