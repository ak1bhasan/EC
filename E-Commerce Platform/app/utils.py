import os
import uuid
from functools import wraps
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from PIL import Image


def allowed_file(filename):
    """Check if file extension is allowed."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    allowed_exts = current_app.config.get(
        "ALLOWED_IMAGE_EXTENSIONS", ["jpg", "jpeg", "png", "webp"]
    )
    return ext in [e.lower() for e in allowed_exts]


def save_product_image(file, create_thumbnail=True):
    """
    Save uploaded product image file.

    Args:
        file: FileStorage object from Flask request
        create_thumbnail: Whether to create a thumbnail version

    Returns:
        str: Filename of saved image
    """
    if not file or not allowed_file(file.filename):
        return None

    # Generate unique filename
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "app/static/uploads")
    filepath = os.path.join(upload_folder, filename)

    # Save original image
    file.save(filepath)

    # Optionally create thumbnail
    if create_thumbnail:
        try:
            img = Image.open(filepath)
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            thumb_filename = f"{uuid.uuid4().hex}_thumb.{ext}"
            thumb_filepath = os.path.join(upload_folder, thumb_filename)
            img.save(thumb_filepath)
        except Exception as e:
            # If thumbnail creation fails, continue without it
            current_app.logger.warning(f"Thumbnail creation failed: {e}")

    return filename


def admin_required(f):
    """Decorator to require admin role."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.admin_login"))
        if not current_user.is_admin:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("products.index"))
        return f(*args, **kwargs)

    return decorated_function


def customer_required(f):
    """Decorator to require customer role (non-admin users)."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        if current_user.is_admin:
            flash("Admin users cannot access customer pages.", "danger")
            return redirect(url_for("admin.dashboard"))
        return f(*args, **kwargs)

    return decorated_function
