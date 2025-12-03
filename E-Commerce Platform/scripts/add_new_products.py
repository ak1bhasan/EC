"""
Add new products to the database.
Run from project root: python scripts/add_new_products.py
"""
from app import create_app
from app.extensions import db
from app.models import Category, Product

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


def add_products():
    """Add new products to the database."""
    app = create_app()
    
    with app.app_context():
        added_count = 0
        skipped_count = 0
        
        for product_data in NEW_PRODUCTS:
            # Find category by name
            category = Category.query.filter_by(name=product_data["category_name"]).first()
            
            if not category:
                print(f"Category '{product_data['category_name']}' not found. Skipping product: {product_data['name']}")
                skipped_count += 1
                continue
            
            # Check if product already exists
            existing_product = Product.query.filter_by(name=product_data["name"]).first()
            if existing_product:
                print(f"Product '{product_data['name']}' already exists. Skipping.")
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
            print(f"Added product: {product_data['name']} (${product_data['price']})")
        
        db.session.commit()
        print(f"\n✅ Successfully added {added_count} products.")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} products (already exist or category not found).")


if __name__ == "__main__":
    add_products()

