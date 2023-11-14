from PIL import Image
import os

def split_png_in_folder(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            # Construct full file path
            file_path = os.path.join(folder_path, filename)

            # Open the image
            with Image.open(file_path) as img:
                width, height = img.size

                # Check if width is the longest side
                if width > height:
                    # Calculate the middle of the image
                    middle = width // 2

                    # Split the image into two parts
                    left_half = img.crop((0, 0, middle, height))
                    right_half = img.crop((middle, 0, width, height))

                    # Save the two halves
                    left_half.save(os.path.join("splitPNG", f'left_half_{filename}'))
                    right_half.save(os.path.join("splitPNG", f'right_half_{filename}'))
                else:
                    print(f"Image {filename} is not wider than it is tall. Skipping.")

# Usage
folder_path = 'outputPNG'  # Replace with the path to your folder containing PNG images
split_png_in_folder(folder_path)
