from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class CartUpdateForm(FlaskForm):
    """Cart item update form."""

    cart_item_id = HiddenField("Cart Item ID", validators=[DataRequired()])
    quantity = IntegerField(
        "Quantity", validators=[DataRequired(), NumberRange(min=0, max=999)]
    )
    submit = SubmitField("Update")


class AddToCartForm(FlaskForm):
    """Add product to cart form."""

    product_id = HiddenField("Product ID", validators=[DataRequired()])
    quantity = IntegerField(
        "Quantity", validators=[DataRequired(), NumberRange(min=1, max=999)], default=1
    )
    submit = SubmitField("Add to Cart")
