import sys
import pandas as pd

sys.path.append("/RIDSS2023/src")
sys.path.append("/RIDSS2023/src/Experiments")
from ocrkit import *
import ocrkit
import sys
import utils
import os
import shutil
from datetime import datetime
from PIL import Image

## Test the impact of different scaling on OCR results

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000

# Path to the input folder with PDF files
input_folder = "/RIDSS2023/src/Experiments/Test_Files/Correct_Rotation_PDFs"

# Create the path for the output folder in which the results are saved
output_folder = "/RIDSS2023/Experiments_Results/Scaling&Resolution/Resize_Test"
# Check if the output folder already exits and delete it if it does
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
# Create the output folder
os.makedirs(output_folder)

# List of supported file extensions
supported_extensions = [".pdf"]

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file has a supported extension
    if any(filename.lower().endswith(ext) for ext in supported_extensions):
        # Full path to the current file
        file_path = os.path.join(input_folder, filename)

        # Create a new InputPDF object
        inputpdf = InputPDF(file_path)

        # Generate the output path for the current file
        file_output_folder = os.path.join(output_folder, filename[:-4])

        # Delete the output folder if it already exists
        if os.path.exists(file_output_folder):
            shutil.rmtree(file_output_folder)

        # Create the output folder
        os.makedirs(file_output_folder)

        # Convert the InputPDF to a TIFF image (300 dpi)
        tiff_image = inputpdf.convert_to_tiff_with_ghostscript(dpi=300)
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
            (20000, 20000),  # Huge
        ]

        # Iterate over the resize sizes
        for width, height in resize_sizes:
            # Initalize the runtime and reset it in each iteration
            runtime_preprocessing = 0
            # Get the start time of preprocessing
            start_time = datetime.now()
            # Resize image
            resized_image = tiff_image.resize(width=width, height=height)
            # Get the runtime by subtracting the start time from the end time
            runtime_preprocessing = datetime.now() - start_time
            # Format the runtime 
            runtime_preprocessing = "{:.2f}".format(runtime_preprocessing.total_seconds())
            resized_image.save_image(
                os.path.join(file_output_folder, f"tiff_image_{width}x{height}px.tiff")
            )

            # Get ocrdata from Tiff Image
            ocrdata = ocrkit.get_ocr_data(
                tiff_image=tiff_image, language="deu+eng+chi_sim"
            )

            # Get Evaluation Data
            evaluation_ocrdata = utils.evaluate_ocrdata(ocrdata)
            # Add the preprocessing runtimes to the DataFrame
            series_runtime = pd.Series(runtime_preprocessing, name='runtime_preprocessing')
            evaluation_ocrdata = pd.concat([evaluation_ocrdata, series_runtime], axis=1)

            # Save evaluation data to Excel
            evaluation_ocrdata.to_excel(
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

