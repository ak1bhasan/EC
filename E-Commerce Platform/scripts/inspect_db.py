"""
Inspect local sqlite dev DB and list products + images.

Run this from the project root `E-Commerce Platform`:

    python .\scripts\inspect_db.py

It checks several likely paths for `dev.db` and prints product rows and product_images.
"""
import os
import sqlite3

possible_paths = [
    os.path.join(os.getcwd(), "dev.db"),
    os.path.join(os.getcwd(), "instance", "dev.db"),
    os.path.join(os.path.dirname(os.getcwd()), "dev.db"),
]


def find_db():
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return None


def inspect_db(path):
    print(f"Using DB: {path}")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM products")
        cnt = cur.fetchone()[0]
        print(f"products count: {cnt}")

        print("\nSample products (id, name):")
        for row in cur.execute("SELECT product_id, name FROM products LIMIT 20"):
            print(row)

        print("\nSample product_images (image_id, product_id, filename, is_main):")
        for row in cur.execute("SELECT image_id, product_id, filename, is_main FROM product_images LIMIT 50"):
            print(row)

    except Exception as e:
        print("SQL error:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = find_db()
    if not db_path:
        print("No dev.db found in common locations. Looked in:")
        for p in possible_paths:
            print("  ", p)
        print("If you ran the seed script from another folder, run it from the project root or move the DB here.")
    else:
        inspect_db(db_path)
