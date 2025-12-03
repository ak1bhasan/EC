"""
Update existing products in the database to set `image_url` values by product name.
Run from the project root with your venv activated:

    venv\\Scripts\\activate
    python scripts\\update_product_images.py

This script will update products if they exist. It does NOT drop or recreate tables.
"""
from app import create_app
from app.extensions import db
from app.models import Product

PRODUCT_IMAGES = {
    "Yoga Mat": "https://images.pexels.com/photos/4325462/pexels-photo-4325462.jpeg",
    "Garden Tools Set": "https://images.pexels.com/photos/20690251/pexels-photo-20690251.jpeg",
    "Web Development Guide": "https://images.pexels.com/photos/4974922/pexels-photo-4974922.jpeg",
    "Python Programming Book": "https://images.pexels.com/photos/1181359/pexels-photo-1181359.jpeg",
    "Jeans": "https://images.pexels.com/photos/52518/jeans-pants-blue-shop-52518.jpeg",
    "T-Shirt": "https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg",
    "Laptop": "https://images.pexels.com/photos/7974/pexels-photo.jpg",
    "Smartphone": "https://images.pexels.com/photos/1786433/pexels-photo-1786433.jpeg",
}


def update_images():
    app = create_app()
    with app.app_context():
        for name, url in PRODUCT_IMAGES.items():
            product = Product.query.filter_by(name=name).first()
            if product:
                product.image_url = url
                db.session.add(product)
                print(f"Updated image_url for product: {name}")
            else:
                print(f"Product not found, skipping: {name}")
        db.session.commit()
        print("Done updating product images.")


if __name__ == '__main__':
    update_images()
