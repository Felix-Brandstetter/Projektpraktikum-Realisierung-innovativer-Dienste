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
import copy

## Test the impact of different binarization methods on OCR results

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000

# Path to the input folder with PDF files
input_folder = "/RIDSS2023/src/Experiments/Test_Files/Correct_Rotation_PDFs"

# Create the path for the output folder in which the results are saved
output_folder = "/RIDSS2023/Experiments_Results/Contrast/Tesseract_binarization_Test"
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

        # Convert the InputPDF to a TIFF image
        tiff_image_original = inputpdf.convert_to_tiff_with_ghostscript(dpi=300)

        # Get ocrdata from Tiff Image
        ocrdata_original = ocrkit.get_ocr_data(
            tiff_image=tiff_image_original, language="deu+eng+chi_sim"
        )
        # Get Evaluation Data
        evaluation_ocrdata_original = utils.evaluate_ocrdata(ocrdata_original)

        # Save to Excel
        evaluation_ocrdata_original.to_excel(
            os.path.join(file_output_folder, f"evaluation_ocrdata_original.xlsx")
        )

        # Create Searchable PDF
        ocrkit.create_searchable_pdf(
            tiff_image=tiff_image_original,
            out_filename=os.path.join(file_output_folder, f"tiff_image_original.pdf"),
            language="deu+eng+chi_sim",
        )
        
        # List the preprocessing methods to be used in the experiment
        methods = [
            "otsu",
            "adaptive_otsu",
            "sauvola"
        ]
        # Iterate over the preprocessing methods
        for method in methods:
            tiff_image = copy.deepcopy(tiff_image_original)
            # Initalize the runtime and reset it in each iteration
            runtime_preprocessing = 0
            # Apply the corresponding preprocessing method
            if method == "otsu":
                # Get ocrdata from Tiff Image
                ocrdata = ocrkit.get_ocr_data(
                    tiff_image=tiff_image, language="deu+eng+chi_sim", tessconfig="-c thresholding_method=0 -c tessedit_write_images=1 -c thresholding_debug=1"
                )
            if method == "adaptive_otsu":
                # Get ocrdata from Tiff Image
                ocrdata = ocrkit.get_ocr_data(
                    tiff_image=tiff_image, language="deu+eng+chi_sim", tessconfig="-c thresholding_method=1 -c tessedit_write_images=1 -c thresholding_debug=1"
                )
            else:
                # Get ocrdata from Tiff Image
                ocrdata = ocrkit.get_ocr_data(
                    tiff_image=tiff_image, language="deu+eng+chi_sim", tessconfig="-c thresholding_method=2 -c tessedit_write_images=1 -c thresholding_debug=1"
                )

            # Get Evaluation Data
            evaluation_ocrdata = utils.evaluate_ocrdata(ocrdata)
            # Add the preprocessing runtime to the DataFrame
            series_runtime = pd.Series(runtime_preprocessing, name='runtime_preprocessing')
            evaluation_ocrdata = pd.concat([evaluation_ocrdata, series_runtime], axis=1)

            # Save to Excel
            evaluation_ocrdata.to_excel(
                os.path.join(file_output_folder, f"evaluation_ocrdata_{method}.xlsx")
            )

            # Create Searchable PDF
            ocrkit.create_searchable_pdf(
                tiff_image=tiff_image,
                out_filename=os.path.join(
                    file_output_folder, f"tiff_image_{method}.pdf"
                ),
                language="deu+eng+chi_sim",
            )
