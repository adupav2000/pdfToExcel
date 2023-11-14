import fitz  # PyMuPDF
import os

def pdf_to_png(pdf_path, output_folder, dpi=300):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            # Get the page
            page = doc.load_page(page_num)

            # Set zoom to maintain the resolution
            zoom = dpi / 72  # 72 is the default DPI for PDFs
            mat = fitz.Matrix(zoom, zoom)

            # Render page to an image (pixmap)
            pix = page.get_pixmap(matrix=mat)

            # Save the image as PNG
            output_path = os.path.join(output_folder, f"page_{page_num}.png")
            pix.save(output_path)

# Usage
pdf_path = 'C:\\Nouveau dossier\\filtered_autoactu_annuaire_automobile_15_2024.pdf'  # Replace with your PDF file path
output_folder = 'outputPNG'  # Replace with your desired output folder path
pdf_to_png(pdf_path, output_folder)
