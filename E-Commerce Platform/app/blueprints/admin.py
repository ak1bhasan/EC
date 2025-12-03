from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app.models import User, Order, Product, Payment
from app.extensions import db, csrf
from app.utils import admin_required
from sqlalchemy import func, desc

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Admin dashboard."""
    # Statistics
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_sales = db.session.query(func.sum(Order.total_price)).scalar() or 0

    # Low stock products (stock < 5)
    low_stock_products = Product.query.filter(Product.stock < 5).all()

    # Latest orders
    latest_orders = Order.query.order_by(desc(Order.order_date)).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_orders=total_orders,
        total_sales=float(total_sales),
        low_stock_products=low_stock_products,
        latest_orders=latest_orders,
    )


@admin_bp.route("/products")
@admin_required
def products():
    """Admin: List all products."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin/products.html", products=products)


@admin_bp.route("/orders")
@admin_required
def orders():
    """Admin: List all orders."""
    orders = Order.query.order_by(desc(Order.order_date)).all()
    return render_template("admin/orders.html", orders=orders)


@admin_bp.route("/order/<int:order_id>/update-status", methods=["POST", "PUT"])
@admin_required
@csrf.exempt
def update_order_status(order_id):
    """Admin: Update order status (supports both form POST and JSON PUT)."""
    order = Order.query.get_or_404(order_id)
    
    # Handle both form data and JSON requests
    if request.is_json:
        data = request.get_json()
        new_status = data.get("status")
    else:
        new_status = request.form.get("status")

    valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    if new_status not in valid_statuses:
        if request.is_json:
            return jsonify({"success": False, "message": "Invalid status."}), 400
        flash("Invalid status.", "danger")
        return redirect(url_for("admin.orders"))

    order.status = new_status
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            "success": True,
            "message": f"Order #{order.order_id} status updated to {new_status}.",
            "status": new_status
        })
    
    flash(f"Order #{order.order_id} status updated to {new_status}.", "success")
    return redirect(url_for("admin.orders"))
