# Quick Start Guide

## One-Line Setup Commands

```bash
# 1. Create virtual environment and activate
python -m venv venv && venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file (copy from .env.example and edit with your MySQL credentials)
copy .env.example .env
# Edit .env and set DATABASE_URI with your MySQL credentials

# 4. Create MySQL database
mysql -u root -p -e "CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 5. Initialize database (choose one method)
# Method A: Using migrations
flask db init && flask db migrate -m "Initial" && flask db upgrade

# Method B: Using SQL file
mysql -u username -p ecommerce_db < sql/schema.sql

# 6. Seed database
python seed.py

# 7. Run application
python run.py
```

## Automated setup (Windows PowerShell)

If you are on Windows you can run the provided PowerShell helper which will create the DB, create a user, import the schema and update `.env`.

From the repository root in PowerShell:

```powershell
.\ackup: Ensure you review the script before running
.\setup_db.ps1
```

The script will prompt for the MySQL `root` password and for the new DB user's password. It will also copy `.env.example` to `.env` and write the `DATABASE_URI` using the `ecom_user` credentials.

Security note: The script writes the database password into `.env` in plain text for convenience — do not commit `.env` to source control.

## Sample .env Configuration

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URI=mysql+pymysql://root:root@localhost:3306/ecommerce
UPLOAD_FOLDER=app/static/uploads
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
MAX_CONTENT_LENGTH=5242880
```

## Default Login Credentials

- **Admin**: `admin@example.com` / `admin123`
- **User**: `user@example.com` / `user123`

## Access the Application

Open your browser and navigate to: `http://localhost:5000`

## Files That May Require Manual Tweaking

- `.env` - Database credentials (REQUIRED)
- `app/static/uploads/` - Product images (add through admin interface)
- `config.py` - Production settings if deploying

## Troubleshooting

### MySQL Connection Issues

- Ensure MySQL server is running
- Verify credentials in `.env`
- Try using `pymysql` if `mysqlclient` fails: `pip install pymysql` and change DATABASE_URI to `mysql+pymysql://...`

### Import Errors

- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Database Errors

- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- Check user permissions
- Verify DATABASE_URI format in `.env`
