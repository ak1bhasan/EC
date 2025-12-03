import click
from flask.cli import with_appcontext
from app import create_app
from app.extensions import db
from app.models import (
    User,
    Category,
    Product,
    ProductImage,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
)
from werkzeug.security import generate_password_hash

app = create_app()


@app.cli.command("create-db")
@with_appcontext
def create_db():
    """Create database tables."""
    db.create_all()
    click.echo("Database tables created.")


@app.cli.command("drop-db")
@with_appcontext
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    click.echo("Database tables dropped.")


@app.cli.command("seed-db")
@with_appcontext
def seed_db():
    """Seed database with initial data."""
    from seed import seed_database

    seed_database()
    click.echo("Database seeded successfully.")


@app.cli.command("update-images")
@with_appcontext
def update_images():
    """Update product image URLs."""
    PRODUCT_IMAGES = {
        "Yoga Mat": "https://images.pexels.com/photos/4325462/pexels-photo-4325462.jpeg",
        "Garden Tools Set": "https://images.pexels.com/photos/20690251/pexels-photo-20690251.jpeg",
        "Web Development Guide": "https://images.pexels.com/photos/4974922/pexels-photo-4974922.jpeg",
        "Python Programming Book": "https://images.pexels.com/photos/1181359/pexels-photo-1181359.jpeg",
        "Jeans": "https://images.pexels.com/photos/52518/jeans-pants-blue-shop-52518.jpeg",
        "T-Shirt": "https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg",
        "Laptop": "https://images.pexels.com/photos/7974/pexels-photo.jpg",
        "Smartphone": "https://images.pexels.com/photos/1786433/pexels-photo-1786433.jpeg",
        # New products
        "Wireless Headphones": "https://images.pexels.com/photos/6686448/pexels-photo-6686448.jpeg",
        "Smart Watch": "https://images.pexels.com/photos/2779018/pexels-photo-2779018.jpeg",
        "Tablet": "https://images.pexels.com/photos/1251844/pexels-photo-1251844.jpeg",
        "Winter Jacket": "https://images.pexels.com/photos/19885905/pexels-photo-19885905.jpeg",
        "Running Shoes": "https://images.pexels.com/photos/601177/pexels-photo-601177.jpeg",
        "Hoodie": "https://images.pexels.com/photos/8217300/pexels-photo-8217300.jpeg",
        "JavaScript Mastery Guide": "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg",
        "Data Science Handbook": "https://images.pexels.com/photos/8383488/pexels-photo-8383488.jpeg",
        "Indoor Plant Set": "https://images.pexels.com/photos/4637542/pexels-photo-4637542.jpeg",
        "Coffee Maker": "https://images.pexels.com/photos/2159106/pexels-photo-2159106.jpeg",
        "Dumbbell Set": "https://images.pexels.com/photos/7743320/pexels-photo-7743320.jpeg",
        "Basketball": "https://images.pexels.com/photos/945471/pexels-photo-945471.jpeg",
    }
    
    updated_count = 0
    for name, url in PRODUCT_IMAGES.items():
        product = Product.query.filter_by(name=name).first()
        if product:
            product.image_url = url
            db.session.add(product)
            click.echo(f"Updated image_url for product: {name}")
            updated_count += 1
        else:
            click.echo(f"Product not found, skipping: {name}")
    
    db.session.commit()
    click.echo(f"Done updating product images. Updated {updated_count} products.")


@app.cli.command("add-products")
@with_appcontext
def add_products():
    """Add new products to the database."""
    # New products to add (without image_url - will be added later)
    NEW_PRODUCTS = [
        # Electronics (3 products)
        {"category_name": "Electronics", "name": "Wireless Headphones", "description": "Premium noise-cancelling wireless headphones with long battery life and superior sound quality.", "price": 149.99, "stock": 35},
        {"category_name": "Electronics", "name": "Smart Watch", "description": "Feature-rich smartwatch with fitness tracking, heart rate monitor, and smartphone connectivity.", "price": 249.99, "stock": 28},
        {"category_name": "Electronics", "name": "Tablet", "description": "10-inch tablet perfect for reading, browsing, and entertainment. High-resolution display.", "price": 399.99, "stock": 22},
        
        # Clothing (3 products)
        {"category_name": "Clothing", "name": "Winter Jacket", "description": "Warm and stylish winter jacket with water-resistant material. Perfect for cold weather.", "price": 89.99, "stock": 45},
        {"category_name": "Clothing", "name": "Running Shoes", "description": "Comfortable athletic running shoes with cushioned sole and breathable mesh upper.", "price": 79.99, "stock": 60},
        {"category_name": "Clothing", "name": "Hoodie", "description": "Soft and cozy hoodie made from premium cotton blend. Available in multiple colors.", "price": 39.99, "stock": 80},
        
        # Books (2 products)
        {"category_name": "Books", "name": "JavaScript Mastery Guide", "description": "Comprehensive guide to mastering JavaScript from basics to advanced concepts.", "price": 42.99, "stock": 18},
        {"category_name": "Books", "name": "Data Science Handbook", "description": "Complete handbook covering data science, machine learning, and data analysis techniques.", "price": 49.99, "stock": 15},
        
        # Home & Garden (2 products)
        {"category_name": "Home & Garden", "name": "Indoor Plant Set", "description": "Set of 3 beautiful indoor plants perfect for home decoration and air purification.", "price": 34.99, "stock": 25},
        {"category_name": "Home & Garden", "name": "Coffee Maker", "description": "Programmable coffee maker with timer and keep-warm function. Makes up to 12 cups.", "price": 69.99, "stock": 30},
        
        # Sports (2 products)
        {"category_name": "Sports", "name": "Dumbbell Set", "description": "Adjustable dumbbell set with multiple weight options. Perfect for home workouts.", "price": 119.99, "stock": 20},
        {"category_name": "Sports", "name": "Basketball", "description": "Official size basketball with premium grip and durability. Suitable for indoor and outdoor use.", "price": 24.99, "stock": 50},
    ]
    
    from app.models import Category
    
    added_count = 0
    skipped_count = 0
    
    for product_data in NEW_PRODUCTS:
        # Find category by name
        category = Category.query.filter_by(name=product_data["category_name"]).first()
        
        if not category:
            click.echo(f"Category '{product_data['category_name']}' not found. Skipping product: {product_data['name']}")
            skipped_count += 1
            continue
        
        # Check if product already exists
        existing_product = Product.query.filter_by(name=product_data["name"]).first()
        if existing_product:
            click.echo(f"Product '{product_data['name']}' already exists. Skipping.")
            skipped_count += 1
            continue
        
        # Create new product (without image_url for now)
        product = Product(
            category_id=category.category_id,
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            stock=product_data["stock"],
            image_url=None  # Will be updated later with image links
        )
        
        db.session.add(product)
        added_count += 1
        click.echo(f"Added product: {product_data['name']} (${product_data['price']})")
    
    db.session.commit()
    click.echo(f"\n✅ Successfully added {added_count} products.")
    if skipped_count > 0:
        click.echo(f"⚠️  Skipped {skipped_count} products (already exist or category not found).")


if __name__ == "__main__":
    app.cli()
