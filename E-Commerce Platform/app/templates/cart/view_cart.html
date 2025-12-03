{% extends "base.html" %}

{% block title %}Shopping Cart - ShopNow{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Shopping Cart</h1>
    </div>
</div>

{% if cart.items %}
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>Total</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in cart.items %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if item.product.images %}
                                                {% set main_image = item.product.images|selectattr('is_main', 'equalto', True)|first or item.product.images[0] %}
                                                <img src="{{ url_for('static', filename='uploads/' + main_image.filename) }}" 
                                                     class="me-2" style="width: 60px; height: 60px; object-fit: cover;">
                                            {% endif %}
                                            <div>
                                                <strong>{{ item.product.name }}</strong>
                                                {% if item.quantity > item.product.stock %}
                                                    <br><small class="text-danger">Only {{ item.product.stock }} available</small>
                                                {% endif %}
                                            </div>
                                        </div>
                                    </td>
                                    <td>${{ "%.2f"|format(item.product.price|float) }}</td>
                                    <td>
                                        <form method="POST" action="{{ url_for('cart.update_cart') }}" class="d-inline">
                                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                                            <input type="hidden" name="cart_item_id" value="{{ item.cart_item_id }}">
                                            <input type="number" name="quantity" value="{{ item.quantity }}" 
                                                   min="0" max="{{ item.product.stock }}" class="form-control form-control-sm" 
                                                   style="width: 80px; display: inline-block;" onchange="this.form.submit()">
                                        </form>
                                    </td>
                                    <td>${{ "%.2f"|format((item.product.price|float * item.quantity)) }}</td>
                                    <td>
                                        <form method="POST" action="{{ url_for('cart.remove_from_cart') }}" class="d-inline">
                                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                                            <input type="hidden" name="cart_item_id" value="{{ item.cart_item_id }}">
                                            <button type="submit" class="btn btn-danger btn-sm">
                                                <i class="bi bi-trash"></i>
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>Order Summary</h5>
                </div>
                <div class="card-body">
                    <table class="table table-sm">
                        <tr>
                            <td>Subtotal:</td>
                            <td class="text-end">${{ "%.2f"|format(cart.get_total()) }}</td>
                        </tr>
                        <tr>
                            <td>Shipping:</td>
                            <td class="text-end">Free</td>
                        </tr>
                        <tr class="border-top">
                            <td><strong>Total:</strong></td>
                            <td class="text-end"><strong>${{ "%.2f"|format(cart.get_total()) }}</strong></td>
                        </tr>
                    </table>
                    <a href="{{ url_for('orders.checkout') }}" class="btn btn-primary w-100">
                        Proceed to Checkout
                    </a>
                </div>
            </div>
        </div>
    </div>
{% else %}
    <div class="alert alert-info">
        <h5>Your cart is empty</h5>
        <p>Start shopping to add items to your cart.</p>
        <a href="{{ url_for('products.index') }}" class="btn btn-primary">Browse Products</a>
    </div>
{% endif %}
{% endblock %}

