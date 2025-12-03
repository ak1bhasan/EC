from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms.order_forms import CheckoutForm
from app.models import Cart, CartItem, Order, OrderItem, Payment, Product
from app.extensions import db
from app.utils import customer_required
from datetime import datetime

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/checkout", methods=["GET", "POST"])
@customer_required
def checkout():
    """Checkout page."""
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()

    if not cart or not cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart.view_cart"))

    form = CheckoutForm()

    if form.validate_on_submit():
        # Calculate total
        total_price = 0
        order_items_data = []

        # Validate stock and prepare order items
        for cart_item in cart.items:
            product = cart_item.product
            if cart_item.quantity > product.stock:
                flash(
                    f"Insufficient stock for {product.name}. Only {product.stock} available.",
                    "danger",
                )
                return redirect(url_for("cart.view_cart"))

            item_total = float(product.price) * cart_item.quantity
            total_price += item_total

            order_items_data.append(
                {
                    "product": product,
                    "quantity": cart_item.quantity,
                    "price": product.price,
                }
            )

        # Create order
        order = Order(
            user_id=current_user.user_id,
            total_price=total_price,
            shipping_address=form.shipping_address.data,
            status="Pending",
        )
        db.session.add(order)
        db.session.flush()  # Get order_id

        # Create order items and update stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item_data["product"].product_id,
                quantity=item_data["quantity"],
                price_at_purchase=item_data["price"],
            )
            db.session.add(order_item)

            # Decrement product stock
            item_data["product"].stock -= item_data["quantity"]

        # Create payment record
        payment = Payment(
            order_id=order.order_id,
            method="Simulated",
            amount=total_price,
            status="Pending",
        )
        db.session.add(payment)

        # Clear cart items
        for cart_item in cart.items:
            db.session.delete(cart_item)

        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for("orders.payment", order_id=order.order_id))

    return render_template("cart/checkout.html", cart=cart, form=form)


@orders_bp.route("/payment/<int:order_id>", methods=["GET", "POST"])
@customer_required
def payment(order_id):
    """Simulated payment page."""
    order = Order.query.get_or_404(order_id)

    # Verify order belongs to current user
    if order.user_id != current_user.user_id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("orders.history"))

    if request.method == "POST":
        # Confirm payment
        payment = order.payment
        if payment:
            payment.status = "Success"
            payment.payment_date = datetime.utcnow()
            if order.status == "Pending":
                order.status = "Processing"
            db.session.commit()
            flash("Payment confirmed successfully!", "success")
            return redirect(url_for("orders.detail", order_id=order.order_id))

    return render_template("order/payment.html", order=order)


@orders_bp.route("/orders")
@customer_required
def history():
    """User order history."""
    orders = (
        Order.query.filter_by(user_id=current_user.user_id)
        .order_by(Order.order_date.desc())
        .all()
    )
    return render_template("order/history.html", orders=orders)


@orders_bp.route("/orders/<int:order_id>")
@login_required
def detail(order_id):
    """Order detail page."""
    order = Order.query.get_or_404(order_id)

    # Verify order belongs to current user or user is admin
    if order.user_id != current_user.user_id and not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("orders.history"))

    return render_template("order/detail.html", order=order)
