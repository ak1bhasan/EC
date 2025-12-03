from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms.cart_forms import CartUpdateForm, AddToCartForm
from app.models import Cart, CartItem, Product
from app.extensions import db
from app.utils import customer_required

cart_bp = Blueprint("cart", __name__)


def get_or_create_cart():
    """Get user's cart or create one if it doesn't exist."""
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart:
        cart = Cart(user_id=current_user.user_id)
        db.session.add(cart)
        db.session.commit()
    return cart


@cart_bp.route("/cart")
@customer_required
def view_cart():
    """View shopping cart."""
    cart = get_or_create_cart()
    return render_template("cart/view_cart.html", cart=cart)


@cart_bp.route("/cart/add", methods=["POST"])
@customer_required
def add_to_cart():
    """Add product to cart."""
    form = AddToCartForm()

    if form.validate_on_submit():
        product_id = form.product_id.data
        quantity = form.quantity.data

        product = Product.query.get_or_404(product_id)

        # Check stock availability
        if quantity > product.stock:
            flash(f"Only {product.stock} items available in stock.", "warning")
            return redirect(url_for("products.detail", product_id=product_id))

        cart = get_or_create_cart()

        # Check if item already in cart
        cart_item = CartItem.query.filter_by(
            cart_id=cart.cart_id, product_id=product_id
        ).first()

        if cart_item:
            # Update quantity (respecting stock)
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                flash(
                    f"Cannot add more. Only {product.stock} items available in stock.",
                    "warning",
                )
                return redirect(url_for("products.detail", product_id=product_id))
            cart_item.quantity = new_quantity
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.cart_id, product_id=product_id, quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()
        flash(f"{product.name} added to cart.", "success")
        return redirect(url_for("cart.view_cart"))

    flash("Invalid form submission.", "danger")
    return redirect(url_for("products.index"))


@cart_bp.route("/cart/update", methods=["POST"])
@customer_required
def update_cart():
    """Update cart item quantity."""
    form = CartUpdateForm()

    if form.validate_on_submit():
        cart_item_id = form.cart_item_id.data
        quantity = form.quantity.data

        cart_item = CartItem.query.get_or_404(cart_item_id)

        # Verify cart belongs to current user
        if cart_item.cart.user_id != current_user.user_id:
            flash("Unauthorized access.", "danger")
            return redirect(url_for("cart.view_cart"))

        if quantity <= 0:
            # Remove item
            db.session.delete(cart_item)
            flash("Item removed from cart.", "info")
        else:
            # Check stock
            if quantity > cart_item.product.stock:
                flash(
                    f"Only {cart_item.product.stock} items available in stock.",
                    "warning",
                )
                return redirect(url_for("cart.view_cart"))
            cart_item.quantity = quantity
            flash("Cart updated.", "success")

        db.session.commit()
        return redirect(url_for("cart.view_cart"))

    flash("Invalid form submission.", "danger")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/remove", methods=["POST"])
@customer_required
def remove_from_cart():
    """Remove item from cart."""
    cart_item_id = request.form.get("cart_item_id", type=int)

    if not cart_item_id:
        flash("Invalid request.", "danger")
        return redirect(url_for("cart.view_cart"))

    cart_item = CartItem.query.get_or_404(cart_item_id)

    # Verify cart belongs to current user
    if cart_item.cart.user_id != current_user.user_id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("cart.view_cart"))

    db.session.delete(cart_item)
    db.session.commit()
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart.view_cart"))
