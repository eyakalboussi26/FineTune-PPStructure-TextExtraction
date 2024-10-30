import os
from PIL import Image
import pytesseract
import pandas as pd

# Define paths
image_path = r"C:\Users\ekalboussi\OneDrive - ALTEN Group\Bureau\Project_NLP\OCR-and-Classifier-Doc\img_3.png"
output_txt_path = r"C:\Users\ekalboussi\OneDrive - ALTEN Group\Bureau\Project_NLP\OCR-and-Classifier-Doc\Classification\file3.txt"

# Ensure Tesseract is installed and available
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ekalboussi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Load the image
image = Image.open(image_path)

# Perform OCR on the image to extract all text
extracted_text = pytesseract.image_to_string(image)

# Split text into sections (rudimentary split based on the structure of the document)
table_text = ""
figure_text = ""
other_text = extracted_text.strip()  # For captions, paragraphs, etc.

# Logic to separate table and figure text from other content
if "min" in extracted_text and "avg" in extracted_text and "max" in extracted_text:
    table_text = extracted_text.split("min")[1].strip()
if "Execution time" in extracted_text:
    figure_text = extracted_text.split("Execution time")[1].strip()

# Save the table to an Excel file (rudimentary processing; adjust as needed)
if table_text:
    # Split rows by newlines, then columns by spaces (adjust for actual format)
    table_data = [line.split() for line in table_text.split("\n") if line.strip()]
    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Use the first row as headers
    table_excel_path = os.path.join(results_folder, "table_output.xlsx")
    df.to_excel(table_excel_path, index=False)

# Save the figure text to a txt file
if figure_text:
    figure_txt_path = os.path.join(results_folder, "figure_output.txt")
    with open(figure_txt_path, 'w', encoding='utf-8') as f:
        f.write(figure_text)

# Optionally print other extracted text (captions/paragraphs)
if other_text:
    print("Other extracted text (captions/paragraphs):")
    print(other_text)

# Save all extracted text to file.txt with UTF-8 encoding
with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(extracted_text)
