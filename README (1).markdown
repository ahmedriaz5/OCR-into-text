# OCR Text Reader with Tkinter GUI

A Python-based OCR (Optical Character Recognition) text reader that extracts text from images using Tesseract OCR and displays the results in a Tkinter GUI. The processed image is shown with green bounding boxes around detected text, and the extracted text appears in a text area. The project uses a predefined `images` folder for input images.

## Features
- **Text Extraction**: Uses Tesseract OCR with preprocessing for accurate text detection.
- **GUI Interface**: Displays the image with text boxes and extracted text in a Tkinter GUI.
- **Predefined Folder**: Uses an `images` folder in the project directory, created automatically.
- **Functionality**:
  - Select an image from the `images` folder to process.
  - Save extracted text to a `.txt` file.
  - Clear the display to reset the GUI.
  - Exit the application.
- **Error Handling**: Handles Tesseract installation issues, invalid images, and file-saving errors.

## Prerequisites
- Python 3.8+
- Tesseract OCR binary
- Python libraries:
  ```bash
  pip install -r requirements.txt
  ```

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ocr-text-reader.git
   cd ocr-text-reader
   ```
2. **Install Tesseract OCR**:
   - **Windows**:
     - Download from [UB-Mannheim Tesseract](https://github