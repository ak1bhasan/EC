from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
import re

try:
    from email_validator import validate_email, EmailNotValidError
    _HAS_EMAIL_VALIDATOR = True
except Exception:
    _HAS_EMAIL_VALIDATOR = False


class SafeEmail:
    """Email validator that uses the `email_validator` package when available.

    Falls back to a simple regex-based check if the package is not installed
    to avoid raising an ImportError during form validation.
    """

    def __init__(self, message=None):
        self.message = message or "Invalid email address."

    def __call__(self, form, field):
        data = field.data or ""
        if _HAS_EMAIL_VALIDATOR:
            try:
                validate_email(data)
                return
            except EmailNotValidError:
                raise ValidationError(self.message)
        # Fallback simple validation
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(pattern, str(data)):
            raise ValidationError(self.message)
from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form."""

    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), SafeEmail()])
    phone = StringField("Phone", validators=[Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is already registered. Please use a different email."
            )


class LoginForm(FlaskForm):
    """Customer login form."""

    email = StringField("Email", validators=[DataRequired(), SafeEmail()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AdminLoginForm(FlaskForm):
    """Admin login form with username and password."""

    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProfileForm(FlaskForm):
    """User profile update form."""

    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField("Phone", validators=[Length(max=20)])
    submit = SubmitField("Update Profile")
