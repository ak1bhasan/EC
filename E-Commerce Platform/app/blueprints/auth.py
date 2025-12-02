from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User, Cart
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for("products.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return render_template("auth/register.html", form=form)

        # Create new user
        user = User(name=form.name.data, email=form.email.data, phone=form.phone.data)
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
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for("products.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("products.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("products.index"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile page."""
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", form=form)
