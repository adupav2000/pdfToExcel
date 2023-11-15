import ocrmypdf
import os
import glob
from PyPDF2 import PdfReader, PdfWriter

def process_png_files(input_folder, output_folder, keyword, image_dpi=300):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all PNG files in the input folder
    png_files = glob.glob(os.path.join(input_folder, '*.png'))

    for png_file in png_files:
        # Convert PNG to PDF
        pdf_path = png_file.replace('.png', '.pdf')
        ocrmypdf.ocr(png_file, pdf_path, deskew=True, image_dpi=image_dpi)

        # Check if the PDF contains the keyword
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if keyword in page_text:
                    # Save the PDF to the output folder
                    output_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path))
                    with open(output_pdf_path, 'wb') as output_file:
                        writer = PdfWriter()
                        writer.add_page(page)
                        writer.write(output_file)
                    break  # No need to check other pages

# Usage
input_folder = './splitPNG'  # Replace with your input folder path
output_folder = './splitAndFilteredPDF'  # Replace with your output folder path
keyword = 'Volume de vente VN'
image_dpi = 300  # Replace with your estimated DPI
process_png_files(input_folder, output_folder, keyword, image_dpi)
