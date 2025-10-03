import cv2
import pytesseract
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Text
from PIL import Image, ImageTk
import os

# Predefined folder for images
image_folder = os.path.join(os.path.dirname(__file__), "images")

# Path to Tesseract executable (update based on your installation)
# For Windows, adjust this path after installing Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Example for Windows
# For Linux/macOS, comment out the above line if Tesseract is in PATH, or set to, e.g., '/usr/bin/tesseract'

def extract_text(image_path):
    try:
        # Load and preprocess image
        image = cv2.imread(image_path)
        if image is None:
            messagebox.showerror("Error", f"Could not load image: {image_path}")
            return None, None
        
        # Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Extract text using Tesseract
        custom_config = r'--oem 3 --psm 6'  # PSM 6 for uniform text block
        extracted_text = pytesseract.image_to_string(thresh, config=custom_config).strip()
        
        # Draw bounding boxes around detected text
        data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 60:  # Confidence threshold
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, data['text'][i], (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Check if text is empty
        if not extracted_text:
            return image, "Text not found"
        
        return image, extracted_text
    except pytesseract.TesseractNotFoundError:
        messagebox.showerror("Error", f"Tesseract executable not found at '{pytesseract.pytesseract.tesseract_cmd}'. "
                                     "Please install Tesseract or update the path in the script. "
                                     "Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        return None, None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during OCR: {str(e)}")
        return None, None

def select_image():
    file_path = filedialog.askopenfilename(initialdir=image_folder, filetypes=[("Images", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image, text = extract_text(file_path)
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image_rgb)
            img = img.resize((320, 240), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            image_label.imgtk = imgtk
            image_label.configure(image=imgtk)
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, text)
            status_label.config(text=f"Image processed: {os.path.basename(file_path)}", fg="green")
        else:
            status_label.config(text="Failed to process image.", fg="red")

def clear_display():
    image_label.imgtk = blank_image
    image_label.configure(image=blank_image)
    text_area.delete(1.0, tk.END)
    status_label.config(text="Display cleared.", fg="red")

def save_text():
    text = text_area.get(1.0, tk.END).strip()
    if not text or text == "Text not found":
        messagebox.showwarning("Warning", "No text to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            status_label.config(text=f"Text saved to {os.path.basename(file_path)}", fg="blue")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text: {str(e)}")

def exit_app():
    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("OCR Text Reader")
root.geometry("800x600")
root.configure(bg="lightblue")

# Blank placeholder image
blank_img = Image.new('RGB', (320, 240), color='black')
blank_image = ImageTk.PhotoImage(blank_img)

# Main frame
main_frame = tk.Frame(root, bg="lightblue")
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Image display
image_label = tk.Label(main_frame, image=blank_image, bg="black")
image_label.pack(side="left", padx=10)

# Right frame for buttons and text
right_frame = tk.Frame(main_frame, bg="lightblue")
right_frame.pack(side="right", fill="y", padx=10)

# Title
title_label = tk.Label(right_frame, text="OCR Text Reader",
                       font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
title_label.pack(pady=10)

# Buttons
btn_select = tk.Button(right_frame, text="Select Image", width=25, command=select_image)
btn_select.pack(pady=5)

btn_save = tk.Button(right_frame, text="Save Text", width=25, command=save_text)
btn_save.pack(pady=5)

btn_clear = tk.Button(right_frame, text="Clear Display", width=25, command=clear_display)
btn_clear.pack(pady=5)

btn_exit = tk.Button(right_frame, text="Exit", width=25, command=exit_app)
btn_exit.pack(pady=5)

# Text area for extracted text
text_area = Text(right_frame, height=10, width=30, font=("Arial", 10))
text_area.pack(pady=10)

# Status label
status_label = tk.Label(right_frame, text="Select an image from the 'images' folder to start...",
                        font=("Arial", 10), bg="lightblue", fg="black")
status_label.pack(pady=20)

# Create images folder if it doesn't exist
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

root.mainloop()