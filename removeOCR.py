import fitz  # PyMuPDF
import glob
import os

def remove_ocr_from_pdf_region(pdf_path, output_path, region, region2):
    """
    Removes OCR text from a specified region in a PDF file.

    Parameters:
    - pdf_path: path to the input PDF file.
    - output_path: path where the output PDF will be saved.
    - region: tuple (x0, y0, x1, y1) defining the rectangle region to clear OCR from.
              The values are given as percentages of the page's width and height.
    """
    # Open the PDF file
    pdf = fitz.open(pdf_path)

    # Iterate over each page in the PDF
    for page in pdf:
        # Calculate the actual coordinates of the region to clear
        # We convert percentages to actual page coordinates here
        x0 = region[0] * page.rect.width
        y0 = region[1] * page.rect.height
        x1 = region[2] * page.rect.width
        y1 = region[3] * page.rect.height
        clear_rect = fitz.Rect(x0, y0, x1, y1)

        # Search for text instances in the specified region
        words = page.get_text("words")  # List of words on the page

        # Check each word to see if it's inside the clear_rect and mark for redaction if so
        for word in words:
            word_rect = fitz.Rect(word[:4])  # Rectangle for the current word
            if clear_rect.intersects(word_rect):  # If the word is inside the clear_rect
                page.add_redact_annot(word_rect)  # Mark the word for redaction

        # Apply the redactions to actually remove the text
        page.apply_redactions()

    for page in pdf:
        # Calculate the actual coordinates of the region to clear
        # We convert percentages to actual page coordinates here
        x0 = region2[0] * page.rect.width
        y0 = region2[1] * page.rect.height
        x1 = region2[2] * page.rect.width
        y1 = region2[3] * page.rect.height
        clear_rect = fitz.Rect(x0, y0, x1, y1)

        # Search for text instances in the specified region
        words = page.get_text("words")  # List of words on the page

        # Check each word to see if it's inside the clear_rect and mark for redaction if so
        for word in words:
            word_rect = fitz.Rect(word[:4])  # Rectangle for the current word
            if clear_rect.intersects(word_rect):  # If the word is inside the clear_rect
                page.add_redact_annot(word_rect)  # Mark the word for redaction

        # Apply the redactions to actually remove the text
        page.apply_redactions()


    # Save the modified PDF
    pdf.save(output_path)
    pdf.close()



# New function to crop all PDFs in a folder
def remove_all_ocr(folder_path, margins, region2):
    # Find all PDF files in the specified directory
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))

    i = 0
    # Loop through all found PDF files and crop them
    for pdf_file in pdf_files:
        file_name, file_extension = os.path.splitext(pdf_file)
        if ("cropped" in file_name):
            output_file = f"./cleanedPDFForV2/{i}_ready{file_extension}"
            remove_ocr_from_pdf_region(pdf_file, output_file, margins, region2)
            print("Processed :", file_name)
            i += 1
        else:
            print("ignored the file : ", file_name, " the content was not cropped")

# Specify the directory containing the PDF files
folder_path = './splitAndFilteredPDF'  # Replace with the actual path to your PDF directory

# Crop all PDFs in the folder

# Define the region to clear OCR from, given as percentages of the page's width and height
# [0% of width, 44.44% of height] to [47.37% of width, 70.37% of height]
region_to_clear = (6 / 9.5, 0 / 13.5, 9.5 / 9.5, 4.5 / 13.5)
region_to_clear_2 = (7.2 / 13.2, 4 / 10.5, 10/10, 5.5 / 10)

remove_all_ocr(folder_path, region_to_clear, region_to_clear_2)