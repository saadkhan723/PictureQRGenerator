# PictureQRGenerator 📸

**A Python and Flask web application to generate QR codes for pictures and website links.**

PictureQRGenerator allows users to upload a picture, provide a direct picture URL, or enter a website link to generate a downloadable QR code. Scan the QR code to access its associated picture or website.

## ✨ Features

- 🖼️ **Upload Picture:** Upload an image and generate its QR code.
- 🔗 **Picture URL to QR:** Paste a direct picture URL and create a QR code that opens a picture-viewing page.
- 🌐 **Website Link to QR:** Generate QR codes for websites and other HTTP/HTTPS links.
- 📥 **Download QR Codes:** Download generated QR codes as PNG images.
- 👀 **Preview:** View the generated QR code before downloading.
- 📱 **Responsive Interface:** Use the application on desktop and mobile browsers.
- 🐍 **Python Backend:** Built using Python and Flask.

## 🛠️ Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- qrcode
- Pillow

## 📂 Project Structure

```text
PictureQRGenerator/
├── app.py
├── requirements.txt
├── .gitignore
├── templates/
│   ├── index.html
│   └── image_page.html
├── static/
│   └── style.css
└── uploads/
    ├── images/
    └── qrcodes/
```

*Note: The exact files and folders may vary depending on your current project setup.*

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/saadkhan723/PictureQRGenerator.git
```

### 2. Open the project directory

```bash
cd PictureQRGenerator
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### 5. Install dependencies

```bash
python -m pip install Flask "qrcode[pil]" Pillow
```

If the project includes a `requirements.txt` file containing all required dependencies, you can instead run:

```bash
python -m pip install -r requirements.txt
```

## 🚀 Run the Application

Start the Flask application:

```bash
python app.py
```

Open your browser and visit:

**http://127.0.0.1:5000**

You can now upload a picture, enter a picture URL, or generate a QR code for a website.

Press `Ctrl + C` in the terminal to stop the application.

## 📖 How to Use

1. Start the application.
2. Select one of the available options:
   - **Upload Picture**
   - **Picture URL**
   - **Website Link**
3. Upload an image or enter a valid URL.
4. Click the appropriate QR generation button.
5. Preview the generated QR code.
6. Download the QR code as a PNG image.
7. Scan the QR code with a phone to open its destination.

## ⚠️ Important Notes

- For picture URLs, use a direct image address rather than a Google Images search-results URL.
- Some image-hosting websites prevent external image embedding, so certain picture URLs may not display correctly.
- QR codes containing `127.0.0.1` or `localhost` work only on the computer running the application. To share them with other people, deploy the application using a publicly accessible URL.
- Uploaded pictures and generated files may not persist on hosting platforms with temporary storage. Use persistent or external storage if permanent file access is required.
- Do not upload your virtual environment, secret credentials, or private files to GitHub.

## 🔮 Future Improvements

- Cloud image storage integration
- QR code customization and color options
- Support for additional image formats
- QR code history and management
- Public deployment with persistent storage
- Improved validation and error handling

## 👨‍💻 Author

**Saad Khan**

GitHub: [@saadkhan723](https://github.com/saadkhan723)

## 📦 Repository

[PictureQRGenerator on GitHub](https://github.com/saadkhan723/PictureQRGenerator)

## 📄 License

This project is available for learning and personal development. Add an appropriate open-source license file if you intend to distribute it under a specific license.

---

⭐ If you find this project useful, consider giving the repository a star on GitHub.

**Built with Python, Flask, and curiosity.**
