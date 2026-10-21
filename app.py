
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

import qrcode
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    url_for,
    abort,
)
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Project folders
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
IMAGE_FOLDER = UPLOAD_FOLDER / "images"
QR_FOLDER = UPLOAD_FOLDER / "qrcodes"

# Create folders automatically
for folder in (IMAGE_FOLDER, QR_FOLDER):
    folder.mkdir(parents=True, exist_ok=True)

# Maximum upload size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def valid_http_url(value):
    """Check that a URL uses HTTP or HTTPS."""
    if not value or any(char.isspace() for char in value):
        return False

    try:
        parsed = urlparse(value)
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
        )
    except ValueError:
        return False


def make_qr(data, qr_name):
    """Create and save a QR code PNG."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    qr_image.save(QR_FOLDER / qr_name)


@app.route("/")
def index():
    return render_template(
        "index.html",
        active_tab="picture",
    )


# -----------------------------------------
# Generate QR for any website link
# -----------------------------------------
@app.route("/generate-link", methods=["POST"])
def generate_link():
    link = request.form.get("link", "").strip()

    if not valid_http_url(link):
        return render_template(
            "index.html",
            error="Please enter a valid link starting with http:// or https://",
            active_tab="link",
        )

    qr_name = f"{uuid.uuid4().hex}.png"
    make_qr(link, qr_name)

    return render_template(
        "index.html",
        qr_url=url_for("download_qr", filename=qr_name),
        qr_preview_url=url_for("preview_qr", filename=qr_name),
        qr_target=link,
        qr_type="link",
        active_tab="link",
    )


# -----------------------------------------
# Generate QR for a picture URL
# QR opens a webpage displaying the picture
# -----------------------------------------
@app.route("/generate-picture-link", methods=["POST"])
def generate_picture_link():
    picture_link = request.form.get(
        "picture_link", ""
    ).strip()

    if not valid_http_url(picture_link):
        return render_template(
            "index.html",
            error="Please enter a valid picture URL starting with http:// or https://",
            active_tab="picture-url",
        )

    # URL of our picture viewing webpage
    page_url = url_for(
        "view_external_picture",
        _external=True,
        image_url=picture_link,
    )

    qr_name = f"{uuid.uuid4().hex}.png"
    make_qr(page_url, qr_name)

    return render_template(
        "index.html",
        qr_url=url_for("download_qr", filename=qr_name),
        qr_preview_url=url_for("preview_qr", filename=qr_name),
        qr_target=page_url,
        qr_type="picture-url",
        image_url=picture_link,
        active_tab="picture-url",
    )


# -----------------------------------------
# Display external picture on a webpage
# -----------------------------------------
@app.route("/view-picture")
def view_external_picture():
    image_url = request.args.get("image_url", "").strip()

    if not valid_http_url(image_url):
        abort(400)

    return render_template(
        "image_page.html",
        image_url=image_url,
    )


# -----------------------------------------
# Upload a picture and generate its QR
# -----------------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "picture" not in request.files:
        return render_template(
            "index.html",
            error="Please select a picture.",
            active_tab="picture",
        )

    file = request.files["picture"]

    if not file or not file.filename:
        return render_template(
            "index.html",
            error="Please select a picture.",
            active_tab="picture",
        )

    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            error="Use PNG, JPG, JPEG or WEBP images only.",
            active_tab="picture",
        )

    extension = file.filename.rsplit(".", 1)[1].lower()
    image_id = uuid.uuid4().hex
    image_name = f"{image_id}.{extension}"
    image_path = IMAGE_FOLDER / image_name

    try:
        # Verify actual image content
        file.stream.seek(0)

        with Image.open(file.stream) as img:
            if img.format not in {"PNG", "JPEG", "WEBP"}:
                raise ValueError("Unsupported image format")

            img.verify()

        file.stream.seek(0)

        with Image.open(file.stream) as img:
            if img.width * img.height > 20_000_000:
                raise ValueError("Image dimensions too large")

        file.stream.seek(0)
        file.save(image_path)

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
    ):
        image_path.unlink(missing_ok=True)

        return render_template(
            "index.html",
            error="Invalid image. Please upload a valid picture.",
            active_tab="picture",
        )

    # URL of the uploaded picture
    picture_url = url_for(
        "serve_image",
        filename=image_name,
        _external=True,
    )

    qr_name = f"{image_id}.png"
    make_qr(picture_url, qr_name)

    return render_template(
        "index.html",
        image_url=picture_url,
        qr_url=url_for("download_qr", filename=qr_name),
        qr_preview_url=url_for("preview_qr", filename=qr_name),
        image_name=secure_filename(file.filename),
        qr_target=picture_url,
        qr_type="picture",
        active_tab="picture",
    )


# -----------------------------------------
# Serve uploaded pictures
# -----------------------------------------
@app.route("/images/<filename>")
def serve_image(filename):
    if not filename or Path(filename).name != filename:
        abort(404)

    response = send_from_directory(
        IMAGE_FOLDER,
        filename,
        as_attachment=False,
    )

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"

    return response


# -----------------------------------------
# Preview QR code
# -----------------------------------------
@app.route("/qr/<filename>")
def preview_qr(filename):
    if not filename or Path(filename).name != filename:
        abort(404)

    return send_from_directory(
        QR_FOLDER,
        filename,
        mimetype="image/png",
        as_attachment=False,
    )


# -----------------------------------------
# Download QR code
# -----------------------------------------
@app.route("/download/<filename>")
def download_qr(filename):
    if not filename or Path(filename).name != filename:
        abort(404)

    return send_from_directory(
        QR_FOLDER,
        filename,
        mimetype="image/png",
        as_attachment=True,
        download_name="qr_code.png",
    )


# -----------------------------------------
# Handle oversized uploads
# -----------------------------------------
@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="Picture is too large. Maximum size is 5 MB.",
        active_tab="picture",
    ), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )
