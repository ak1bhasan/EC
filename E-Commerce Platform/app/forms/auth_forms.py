from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form."""

    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
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
    """User login form."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProfileForm(FlaskForm):
    """User profile update form."""

    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField("Phone", validators=[Length(max=20)])
    submit = SubmitField("Update Profile")
