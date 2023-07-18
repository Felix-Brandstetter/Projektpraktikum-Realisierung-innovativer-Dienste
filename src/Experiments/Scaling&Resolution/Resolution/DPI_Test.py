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

## Test the impact of different resolutions on OCR results

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000

# Path to the input folder with PDF files
input_folder = "/RIDSS2023/src/Experiments/Test_Files/Correct_Rotation_PDFs"

# Create the path for the output folder in which the results are saved
output_folder = "/RIDSS2023/Experiments_Results/Scaling&Resolution/DPI_Test"
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

        # List the different DPIs to be used in the experiment
        dpi_list = [72, 150, 300, 600, 1200, 2400]
        # Iterate over the different DPIs
        for dpi in dpi_list:
            # Initalize the runtime and reset it in each iteration
            runtime_preprocessing = 0
            # Get the start time of preprocessing
            start_time = datetime.now()
            # Convert the InputPDF to a TIFF image using the corresponding DPI
            tiff_image = inputpdf.convert_to_tiff_with_ghostscript(dpi=dpi)
            # Get the runtime by subtracting the start time from the end time
            runtime_preprocessing = datetime.now() - start_time
            # Format the runtime 
            runtime_preprocessing = "{:.2f}".format(runtime_preprocessing.total_seconds())
            #Resize Image to fit A4 Page. 3508 pixels correspond to large site of A4 page.
            tiff_image = tiff_image.resize(width=3508, height=3508)
            tiff_image.save_image(
                os.path.join(file_output_folder, f"tiff_image_{dpi}_dpi.tiff")
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

            # Save to Excel
            evaluation_ocrdata.to_excel(
                os.path.join(file_output_folder, f"evaluation_ocrdata_{dpi}_dpi.xlsx")
            )

            # Create Searchable PDF
            ocrkit.create_searchable_pdf(
                tiff_image=tiff_image,
                out_filename=os.path.join(
                    file_output_folder, f"tiff_image_{dpi}_dpi.pdf"
                ),
                language="deu+eng+chi_sim",
            )

