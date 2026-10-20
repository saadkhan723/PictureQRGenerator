
import uuid
from pathlib import Path

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "picture" not in request.files:
        return render_template(
            "index.html",
            error="Please select a picture."
        )

    file = request.files["picture"]

    if not file or not file.filename:
        return render_template(
            "index.html",
            error="Please select a picture."
        )

    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            error="Use PNG, JPG, JPEG or WEBP images only."
        )

    # Generate a unique filename
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
            width, height = img.size

            if width * height > 20_000_000:
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
            error="Invalid image. Please upload a valid picture."
        )

    # URL that opens the uploaded picture
    picture_url = url_for(
        "serve_image",
        filename=image_name,
        _external=True,
    )

    # Generate QR Code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(picture_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    qr_name = f"{image_id}.png"
    qr_image.save(QR_FOLDER / qr_name)

    # Show result on website
    return render_template(
        "index.html",
        image_url=picture_url,
        qr_url=url_for(
            "download_qr",
            filename=qr_name,
        ),
        qr_preview_url=url_for(
            "preview_qr",
            filename=qr_name,
        ),
        image_name=secure_filename(file.filename),
    )


# Open uploaded picture
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


# Display QR Code in browser
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


# Download QR Code as PNG
@app.route("/download/<filename>")
def download_qr(filename):
    if not filename or Path(filename).name != filename:
        abort(404)

    return send_from_directory(
        QR_FOLDER,
        filename,
        mimetype="image/png",
        as_attachment=True,
        download_name="picture_qr.png",
    )


# Handle files larger than 5 MB
@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="Picture is too large. Maximum size is 5 MB.",
    ), 413


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
