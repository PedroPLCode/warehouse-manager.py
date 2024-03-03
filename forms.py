from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ProductAddForm(FlaskForm):
    name = StringField('Name', 
                       validators=[DataRequired()])
    quantity = DecimalField('Quantity', 
                            validators=[DataRequired(), 
                                        NumberRange(min=0, 
                                                    message=None)])
    unit = SelectField('Unit', 
                       validators=[DataRequired()],
                       choices=[('m', 'm'), 
                                ('kg', 'kg'), 
                                ('pcs', 'pcs'), 
                                ('box', 'box'), 
                                ('pallet', 'pallet')])
    unit_price = DecimalField('Unit price',
                              validators=[DataRequired(), 
                                          NumberRange(min=0, 
                                                      message=None)])
    
class ProductSaleForm(FlaskForm):
    quantity_to_sell = DecimalField('Quantity to sell', 
                                    validators=[DataRequired(), 
                                                NumberRange(min=0, 
                                                            message=None)])