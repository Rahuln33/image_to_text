import pytesseract
from PIL import Image
import fitz  # PyMuPDF

# Path to the Tesseract executable (change this if it's different on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the PDF file
pdf_path = 'image_1_1.jpeg'

# Function to extract text from each page of the PDF using OCR
def extract_text_from_page(page):
    # Render the page as an image
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Perform OCR on the image
    text = pytesseract.image_to_string(img)

    return text

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Function to extract key-value pairs from text
def extract_key_value_pairs(text):
    key_value_pairs = {}
    lines = text.split('\n')
    for line in lines:
        # Split each line into key-value pair based on ':'
        parts = line.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            key_value_pairs[key] = value
    return key_value_pairs

# Iterate through each page of the PDF and extract text
all_key_value_pairs = []
for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)
    text = extract_text_from_page(page)
    key_value_pairs = extract_key_value_pairs(text)
    all_key_value_pairs.append(key_value_pairs)

# Close the PDF document
pdf_document.close()

# Store the key-value pairs in a text file
output_file_path = 'extracted_key_value_pairs.txt'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for index, key_value_pairs in enumerate(all_key_value_pairs):
        output_file.write(f"Page {index + 1}:\n")
        for key, value in key_value_pairs.items():
            output_file.write(f"{key}: {value}\n")
        output_file.write("="*50 + "\n")

print(f"Extracted key-value pairs saved to: {output_file_path}")
