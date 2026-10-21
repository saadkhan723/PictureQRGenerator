# PictureQRGenerator 📸

**A simple and user-friendly QR Code Generator built with Python and Flask.**

PictureQRGenerator allows users to generate QR codes for uploaded pictures, direct picture URLs, and website links. Download the generated QR code as a PNG image and share it easily.

## ✨ Features

- 🖼️ **Upload Picture:** Upload a picture and generate its QR code.
- 🔗 **Picture URL:** Paste a direct picture URL to generate a QR code that opens a webpage displaying the picture.
- 🌐 **Website QR Code:** Generate QR codes for websites, YouTube, and other HTTP/HTTPS links.
- 📥 **Download QR Code:** Download generated QR codes in PNG format.
- 👀 **Preview:** Preview generated QR codes and uploaded pictures.
- 📱 **Responsive Interface:** Simple interface designed for convenient use.
- 🐍 **Python & Flask:** Built using Python, Flask, Pillow, and the qrcode library.

## 🛠️ Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- Pillow
- Python `qrcode` library

## 📁 Project Structure

```text
PictureQRGenerator/
├── app.py
├── templates/
│   ├── index.html
│   └── image_page.html
├── static/
│   └── style.css
├── uploads/
│   ├── images/
│   └── qrcodes/
├── .gitignore
└── README.md
```

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

```bat
.venv\Scripts\activate.bat
```

### 5. Install the required libraries

```bash
python -m pip install Flask Pillow "qrcode[pil]"
```

### 6. Run the application

```bash
python app.py
```

### 7. Open the application

Visit this address in your browser:

```text
http://127.0.0.1:5000
```

## 🚀 How to Use

### Option 1: Upload a Picture

1. Open the application.
2. Select **Upload Picture**.
3. Choose a supported picture file.
4. Generate the QR code.
5. Preview and download the QR code.

### Option 2: Generate a Picture URL QR Code

1. Select **Picture URL**.
2. Paste a direct URL to an online picture.
3. Generate the QR code.
4. Scan it to open the picture webpage.

### Option 3: Generate a Website QR Code

1. Select **Website Link**.
2. Paste a valid website URL, such as `https://www.youtube.com/`.
3. Generate and download the QR code.
4. Scan the code to open the destination website.

## 🖼️ Supported Picture Formats

- PNG
- JPG
- JPEG
- WEBP

The picture upload form is configured for a maximum file size of 5 MB.

## ⚠️ Important Notes

- Use a direct picture URL rather than a Google Images search-results URL.
- Some websites restrict external picture display, so certain picture URLs may not work.
- When running locally, uploaded-picture QR codes use your local application address. Other devices cannot access that address unless the application is reachable through a suitable network or public deployment.
- To share uploaded-picture QR codes publicly, deploy the application to a public server and use persistent image storage if uploaded files must survive server restarts.

## 🔮 Future Improvements

- Cloud image storage integration
- User accounts and QR code history
- Custom QR code colors and designs
- Logo support inside QR codes
- Improved deployment and production configuration

## 👨‍💻 Author

**Saad Khan**

GitHub: [@saadkhan723](https://github.com/saadkhan723)

## 📄 License

This project is available for learning and personal use. Add a formal open-source license if you want to specify permissions for redistribution and reuse.
