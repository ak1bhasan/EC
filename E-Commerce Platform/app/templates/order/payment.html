{% extends "base.html" %}

{% block title %}Payment - Order #{{ order.order_id }} - ShopNow{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">Payment Confirmation</h3>
            </div>
            <div class="card-body">
                <h5>Order Summary</h5>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in order.items %}
                            <tr>
                                <td>{{ item.product.name }}</td>
                                <td>{{ item.quantity }}</td>
                                <td>${{ "%.2f"|format(item.price_at_purchase|float) }}</td>
                                <td>${{ "%.2f"|format((item.price_at_purchase|float * item.quantity)) }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot>
                        <tr class="border-top">
                            <th colspan="3">Total Amount:</th>
                            <th>${{ "%.2f"|format(order.total_price|float) }}</th>
                        </tr>
                    </tfoot>
                </table>
                
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i> This is a simulated payment system. Click the button below to confirm payment.
                </div>
                
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                    <div class="d-grid">
                        <button type="submit" class="btn btn-success btn-lg">
                            <i class="bi bi-check-circle"></i> Confirm Payment
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

