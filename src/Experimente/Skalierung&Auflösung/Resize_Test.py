import sys

sys.path.append("/RIDSS2023/src")
sys.path.append("/RIDSS2023/src/Experimente")
from ocrkit import *
import ocrkit
import sys
import utils
import os
import shutil
from datetime import datetime
from PIL import Image

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000

# Define input folder
input_folder = "/RIDSS2023/src/Experimente/Testdateien"

# Create output folder
output_folder = "/RIDSS2023/experiment_ergebnisse/Skalierung&Auflösung/Resize_Test"
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

# Process all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        input_file = os.path.join(input_folder, filename)

        # Erzeuge den Ausgabepfad für die aktuellen Datei
        file_output_folder = os.path.join(output_folder, filename[:-4])

        # Lösche den Ausgabeordner, falls er bereits existiert
        if os.path.exists(file_output_folder):
            shutil.rmtree(file_output_folder)

        # Erstelle den Ausgabeordner
        os.makedirs(file_output_folder)

        # Load input PDF
        input_pdf = InputPDF(input_file)

        # Convert to TIFF image (300 dpi)
        tiff_image = input_pdf.convert_to_tiff_with_ghostscript(dpi=300)
        tiff_image.save_image(os.path.join(file_output_folder, "original_size.tiff"))

        # Define resize sizes
        resize_sizes = [
            (874, 1240),  # A7
            (1240, 1748),  # A6
            (1748, 2480),  # A5
            (2480, 3508),  # A4
            (3508, 4961),  # A3
            (4961, 7016),  # A2
            (7016, 9933),  # A1
            (9933, 14043),  # A0
            (20000, 20000),  # Riesig
        ]

        for width, height in resize_sizes:
            # Resize image
            resized_image = tiff_image.resize(width=width, height=height)
            resized_image.save_image(
                os.path.join(file_output_folder, f"tiff_image_{width}x{height}px.tiff")
            )

            # Get OCR data
            ocrdata = ocrkit.get_ocr_data(resized_image, language="deu+eng+chi_sim")

            # Evaluate OCR data
            evaluation_data = utils.evaluate_ocrdata(ocrdata)

            # Save evaluation data to Excel
            evaluation_data.to_excel(
                os.path.join(
                    file_output_folder, f"evaluation_ocrdata_{width}x{height}px.xlsx"
                )
            )

            # Create searchable PDF
            ocrkit.create_searchable_pdf(
                resized_image,
                os.path.join(file_output_folder, f"tiff_image_{width}x{height}px.pdf"),
                language="deu+eng+chi_sim",
            )
