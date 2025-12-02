from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CheckoutForm(FlaskForm):
    """Checkout form for shipping address."""

    shipping_address = TextAreaField(
        "Shipping Address",
        validators=[DataRequired(), Length(min=10, max=500)],
        render_kw={"rows": 4, "placeholder": "Enter your complete shipping address"},
    )
    submit = SubmitField("Place Order")
