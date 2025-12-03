from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import RegistrationForm, LoginForm, ProfileForm, AdminLoginForm
from app.models import User, Cart
from app.extensions import db, csrf
from app.utils import customer_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Customer registration (admin cannot register)."""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("products.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return render_template("auth/register.html", form=form)

        # Create new customer user (role defaults to 'user')
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            phone=form.phone.data,
            role="user"  # Explicitly set as customer
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        # Create cart for user
        cart = Cart(user_id=user.user_id)
        db.session.add(cart)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Customer login."""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("products.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            # Check if user is admin trying to login as customer
            if user.is_admin:
                flash("Admin users must use the admin login page.", "danger")
                return render_template("auth/login.html", form=form, login_type="customer")
            
            login_user(user, remember=True)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("products.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form, login_type="customer")


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login with hardcoded credentials."""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("products.index"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        # Hardcoded admin credentials
        ADMIN_USERNAME = "Akib Hasan"
        ADMIN_PASSWORD = "CSE_123"
        
        # Check credentials exactly
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            # Find or create admin user in database
            admin_user = User.query.filter_by(email="admin@example.com").first()
            if not admin_user:
                # Create admin user if doesn't exist
                admin_user = User(
                    name=ADMIN_USERNAME,
                    email="admin@example.com",
                    role="admin"
                )
                admin_user.set_password(ADMIN_PASSWORD)
                db.session.add(admin_user)
                db.session.commit()
            else:
                # Update admin user name and password if exists
                admin_user.name = ADMIN_USERNAME
                admin_user.set_password(ADMIN_PASSWORD)
                admin_user.role = "admin"
                db.session.commit()
            
            login_user(admin_user, remember=True)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid admin credentials.", "danger")

    return render_template("auth/login.html", form=form, login_type="admin")


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
@csrf.exempt
def logout():
    """User logout - supports both GET and POST."""
    try:
        logout_user()
        flash("You have been logged out.", "info")
    except Exception as e:
        # Log error but still redirect
        print(f"Logout error: {e}")
        flash("Logged out successfully.", "info")
    return redirect(url_for("products.index"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@customer_required
def profile():
    """Customer profile page (admin cannot access)."""
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", form=form)
