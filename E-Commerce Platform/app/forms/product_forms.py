from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectField,
    MultipleFileField,
    SubmitField,
)
from wtforms.validators import DataRequired, NumberRange
from app.models import Category


class ProductForm(FlaskForm):
    """Product create/edit form."""

    name = StringField("Product Name", validators=[DataRequired()])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    price = DecimalField(
        "Price", validators=[DataRequired(), NumberRange(min=0.01)], places=2
    )
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField("Description", validators=[])
    images = MultipleFileField(
        "Product Images",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only!")],
    )
    submit = SubmitField("Save Product")

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Populate category choices
        self.category_id.choices = [
            (c.category_id, c.name)
            for c in Category.query.order_by(Category.name).all()
        ]
