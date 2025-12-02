"""
Diagnostic: check database URI and whether products.image_url column exists.
Run with the project's venv active.
"""
import os
from sqlalchemy import create_engine, inspect

# Load DATABASE_URI from environment if set, otherwise use config.DevConfig default
from config import DevConfig

db_uri = os.environ.get("DATABASE_URI") or DevConfig.SQLALCHEMY_DATABASE_URI
print("Using DB URI:", db_uri)

engine = create_engine(db_uri)
inspector = inspect(engine)

print("Tables:", inspector.get_table_names())
if "products" in inspector.get_table_names():
    cols = [c["name"] for c in inspector.get_columns("products")]
    print("products columns:", cols)
else:
    print("products table not found")
