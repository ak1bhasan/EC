from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)
from flask_login import login_required
from app.forms.product_forms import ProductForm
from app.forms.cart_forms import AddToCartForm
from app.models import Product, Category
from app.extensions import db
from app.utils import admin_required


products_bp = Blueprint("products", __name__)


@products_bp.route("/")
@products_bp.route("/products")
def index():
    page = request.args.get("page", 1, type=int)
    products = (
        Product.query.order_by(Product.created_at.desc())
        .paginate(page=page, per_page=9, error_out=False)
    )
    return render_template("product/list.html", products=products)


@products_bp.route("/product/<int:product_id>")
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    form.product_id.data = product_id
    return render_template("product/detail.html", product=product, form=form)


@products_bp.route("/admin/product/new", methods=["GET", "POST"])
@admin_required
def admin_create():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            category_id=form.category_id.data,
            price=form.price.data,
            stock=form.stock.data,
            description=form.description.data,
        )
        db.session.add(product)
        db.session.commit()
        flash("Product created successfully.", "success")
        return redirect(url_for("admin.products"))

    return render_template("product/admin_edit.html", form=form, product=None)


@products_bp.route("/admin/product/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for("admin.products"))

    return render_template("product/admin_edit.html", form=form, product=product)


@products_bp.route("/admin/product/<int:product_id>/delete", methods=["POST"])
@admin_required
def admin_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "success")
    return redirect(url_for("admin.products"))
