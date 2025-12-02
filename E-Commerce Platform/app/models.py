from datetime import datetime
from flask_login import UserMixin
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User model with authentication support."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(
        db.Enum("user", "admin", name="user_role"), default="user", nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    carts = db.relationship(
        "Cart", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    orders = db.relationship("Order", backref="user", lazy=True)

    def get_id(self):
        """Return user_id for Flask-Login compatibility."""
        return str(self.user_id)

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """Check if user is admin."""
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.email}>"


class Category(db.Model):
    """Product category model."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    products = db.relationship(
        "Product", backref="category", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    """Product model."""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.category_id"), nullable=False
    )
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    images = db.relationship(
        "ProductImage", backref="product", lazy=True, cascade="all, delete-orphan"
    )
    cart_items = db.relationship("CartItem", backref="product", lazy=True)
    order_items = db.relationship("OrderItem", backref="product", lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"


class ProductImage(db.Model):
    """Product image model."""

    __tablename__ = "product_images"

    image_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    filename = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ProductImage {self.filename}>"


class Cart(db.Model):
    """Shopping cart model."""

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    items = db.relationship(
        "CartItem", backref="cart", lazy=True, cascade="all, delete-orphan"
    )

    def get_total(self):
        """Calculate total cart value."""
        total = 0
        for item in self.items:
            total += float(item.product.price) * item.quantity
        return total

    def __repr__(self):
        return f"<Cart {self.cart_id} for User {self.user_id}>"


class CartItem(db.Model):
    """Cart item model."""

    __tablename__ = "cart_items"

    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CartItem {self.cart_item_id}>"


class Order(db.Model):
    """Order model."""

    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(
        db.Enum(
            "Pending",
            "Processing",
            "Shipped",
            "Delivered",
            "Cancelled",
            name="order_status",
        ),
        default="Pending",
        nullable=False,
    )
    shipping_address = db.Column(db.Text, nullable=False)

    # Relationships
    items = db.relationship(
        "OrderItem", backref="order", lazy=True, cascade="all, delete-orphan"
    )
    payment = db.relationship(
        "Payment", backref="order", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order {self.order_id}>"


class OrderItem(db.Model):
    """Order item model."""

    __tablename__ = "order_items"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<OrderItem {self.order_item_id}>"


class Payment(db.Model):
    """Payment model."""

    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer, db.ForeignKey("orders.order_id"), unique=True, nullable=False
    )
    method = db.Column(db.String(50), default="Simulated", nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(
        db.Enum("Pending", "Success", "Failed", name="payment_status"),
        default="Pending",
        nullable=False,
    )
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.payment_id}>"
