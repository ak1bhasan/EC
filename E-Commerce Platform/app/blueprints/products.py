from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
)
from flask_login import login_required
from app.forms.product_forms import ProductForm
from app.forms.cart_forms import AddToCartForm
from app.models import Product, Category
from app.extensions import db, csrf
from app.utils import admin_required


products_bp = Blueprint("products", __name__)


@products_bp.route("/")
@products_bp.route("/products")
def index():
    page = request.args.get("page", 1, type=int)
    products = (
        Product.query.order_by(Product.created_at.desc())
        .paginate(page=page, per_page=12, error_out=False)
    )
    return render_template("product/list.html", products=products)


@products_bp.route("/product/<int:product_id>")
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    form.product_id.data = product_id
    return render_template("product/detail.html", product=product, form=form)


@products_bp.route("/products/add", methods=["POST"])
@csrf.exempt
def add():
    """Add a new product via AJAX."""
    try:
        data = request.get_json()
        
        # Validate required fields
        errors = {}
        if not data.get('name') or not data.get('name').strip():
            errors['name'] = 'Product name is required'
        if not data.get('price') or float(data.get('price', 0)) <= 0:
            errors['price'] = 'Price must be greater than 0'
        if not data.get('stock_status'):
            errors['stock_status'] = 'Stock status is required'
        if data.get('stock_status') == 'in_stock':
            stock = int(data.get('stock', 0))
            if stock < 0:
                errors['stock'] = 'Stock quantity must be 0 or greater'
        if not data.get('image_url') or not data.get('image_url').strip():
            errors['image_url'] = 'Image URL is required'
        if not data.get('category') or not data.get('category').strip():
            errors['category'] = 'Category is required'
        
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Find or create category
        category_name = data.get('category').strip()
        category = Category.query.filter_by(name=category_name).first()
        
        if not category:
            # Create category with slug
            slug = category_name.lower().replace(' ', '-').replace('&', 'and')
            # Ensure slug is unique
            base_slug = slug
            counter = 1
            while Category.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            category = Category(name=category_name, slug=slug)
            db.session.add(category)
            db.session.flush()
        
        # Determine stock value
        stock_value = int(data.get('stock', 0)) if data.get('stock_status') == 'in_stock' else 0
        
        # Create product
        product = Product(
            name=data.get('name').strip(),
            category_id=category.category_id,
            price=float(data.get('price')),
            stock=stock_value,
            description=data.get('description', '').strip(),
            image_url=data.get('image_url').strip()
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product added successfully',
            'product_id': product.product_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error adding product: {str(e)}'
        }), 500


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
