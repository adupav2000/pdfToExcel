import ocrmypdf
import os
import glob
from PyPDF2 import PdfFileReader, PdfFileWriter

def process_png_files(input_folder, output_folder, keyword):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all PNG files in the input folder
    png_files = glob.glob(os.path.join(input_folder, '*.png'))

    for png_file in png_files:
        # Convert PNG to PDF
        pdf_path = png_file.replace('.png', '.pdf')
        ocrmypdf.ocr(png_file, pdf_path, deskew=True)

        # Check if the PDF contains the keyword
        with open(pdf_path, 'rb') as f:
            reader = PdfFileReader(f)
            for page_num in range(reader.getNumPages()):
                page = reader.getPage(page_num)
                page_text = page.extractText()
                if keyword in page_text:
                    # Save the PDF to the output folder
                    output_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path))
                    with open(output_pdf_path, 'wb') as output_file:
                        writer = PdfFileWriter()
                        writer.addPage(page)
                        writer.write(output_file)
                    break  # No need to check other pages

# Usage# Usage
input_folder = 'C:\\Nouveau dossier\\splitPNG'  # Replace with your input folder path
output_folder = 'C:\\Nouveau dossier\\splitAndFilteredPDF'  # Replace with your output folder path
keyword = 'Volume de vente VN'
process_png_files(input_folder, output_folder, keyword)
