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


if __name__ == "__main__":
    app.cli()
