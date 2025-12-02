# E-Commerce Platform

A complete Flask-based e-commerce platform with server-side rendered templates, MySQL database, and admin panel.

## Tech Stack

- **Backend**: Flask 2.1+ (App Factory Pattern)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login with session-based auth, Werkzeug password hashing
- **Templates**: Jinja2 with Bootstrap 5
- **Forms**: Flask-WTF with CSRF protection
- **File Upload**: Pillow for image processing
- **Migrations**: Flask-Migrate

## Features

- User authentication (register, login, logout, profile)
- Product catalog with search, filtering, and sorting
- Shopping cart with persistent storage
- Order management system
- Simulated payment processing
- Admin dashboard for managing products and orders
- Multiple product images support
- Stock management
- Order tracking

## Project Structure

```
ecommerce-flask/
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── run.py
├── manage.py
├── config.py
├── seed.py
├── sql/
│   ├── schema.sql
│   └── seed.sql
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── utils.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── product_forms.py
│   │   ├── cart_forms.py
│   │   └── order_forms.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── layout/
│   │   ├── auth/
│   │   ├── product/
│   │   ├── cart/
│   │   ├── order/
│   │   └── admin/
│   └── static/
│       ├── css/
│       ├── js/
│       └── uploads/
└── tests/
    └── test_basic.py
```

## Local Setup Instructions

### Prerequisites

- Python 3.10 or higher
- MySQL Server installed and running
- pip (Python package manager)

### Step 1: Clone and Navigate

```bash
cd "X:\E-Commerce Platform Akib"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If `mysqlclient` installation fails on Windows, you may need to install MySQL Connector/C or use `pymysql` instead. For Windows, you can try:

```bash
pip install pymysql
```

Then modify `config.py` to use `mysql+pymysql://` instead of `mysql://` in the DATABASE_URI.

### Step 4: Configure Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and update the following:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URI=mysql+pymysql://root:root@localhost:3306/ecommerce
UPLOAD_FOLDER=app/static/uploads
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
MAX_CONTENT_LENGTH=5242880
```

**Important**: Replace `root`, `root`, and `ecommerce` with your MySQL credentials and desired database name if they differ.

### Step 5: Create MySQL Database

Log into MySQL and create the database:

```bash
mysql -u root -p < create_database.sql
```

### Step 6: Initialize Database

You have two options:

**Option A: Using Flask-Migrate (Recommended)**

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Option B: Using SQL Schema File**

```bash
mysql -u username -p ecommerce_db < sql/schema.sql
```

### Step 7: Seed Database

Run the seed script to create admin user and sample data:

```bash
python seed.py
```

This will create:

- Admin user: `admin@example.com` / `admin123`
- Test user: `user@example.com` / `user123`
- Sample categories and products

### Step 8: Run the Application

```bash
# Option 1: Using run.py
python run.py

# Option 2: Using Flask CLI
flask run
```

The application will be available at `http://localhost:5000`

## Default Credentials

After seeding:

- **Admin**: `admin@example.com` / `admin123`
- **User**: `user@example.com` / `user123`

**Important**: Change these passwords in production!

## Usage

### As a Customer

1. Register a new account or login with test credentials
2. Browse products on the homepage
3. Use search and filters to find products
4. View product details and add items to cart
5. Proceed to checkout and place orders
6. View order history and track order status

### As an Admin

1. Login with admin credentials
2. Access Admin Dashboard from the navbar
3. Manage products (add, edit, delete, upload images)
4. View and manage orders (update order status)
5. Monitor sales statistics and low stock items

## Adding Product Images

1. Login as admin
2. Navigate to Admin > Products
3. Click "Add New Product" or edit existing product
4. Select image files (jpg, jpeg, png, webp)
5. First image will be set as main image
6. Images are stored in `app/static/uploads/`

## Running Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
pytest tests/

# Run with verbose output
pytest tests/ -v
```

## Database Migrations

When making model changes:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Troubleshooting

### MySQL Connection Issues

- Ensure MySQL server is running
- Verify database credentials in `.env`
- Check MySQL user has proper permissions
- Try using `pymysql` driver if `mysqlclient` fails

### Image Upload Issues

- Ensure `app/static/uploads/` directory exists and is writable
- Check file size limits in `.env` (MAX_CONTENT_LENGTH)
- Verify allowed file extensions

### Import Errors

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.10+ required)

## Production Deployment Notes

Before deploying to production:

1. Change `SECRET_KEY` in `.env` to a strong random value
2. Set `FLASK_ENV=production`
3. Use a production WSGI server (e.g., Gunicorn, uWSGI)
4. Configure proper database backups
5. Set up HTTPS/SSL
6. Configure proper file storage (consider cloud storage for images)
7. Review and harden security settings
8. Change default admin credentials

## Files That May Require Manual Tweaking

- `.env` - Database credentials and configuration
- `app/static/uploads/` - Product images (add through admin interface)
- `config.py` - Production configuration settings
- Database connection string format if using different MySQL drivers

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please check:

- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy documentation: https://docs.sqlalchemy.org/
- Bootstrap 5 documentation: https://getbootstrap.com/docs/5.3/
