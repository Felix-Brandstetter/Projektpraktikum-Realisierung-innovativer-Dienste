import sys

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

## Test the impact of different languages on OCR results 

# Path to the input folder with PDF files
input_folder = "/RIDSS2023/src/Experiments/Test_Files/Correct_Rotation_PDFs"

# Create the path for the output folder in which the results are saved
output_folder = "/RIDSS2023/Experiments_Results/Language/Language_Test"
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
        tiff_image = inputpdf.convert_to_tiff_with_ghostscript(dpi=300)
        tiff_image.save_image(os.path.join(file_output_folder, "tiff_image_300_dpi.tiff"))

        # Define the languages to be used in the experiment 
        languages = ["eng", "deu", "chi_sim","deu+eng+chi_sim","ita+ara+fin+dan+fra+hin+spa+por+deu+eng+chi_sim","eng+chi_sim","eng+deu"]

        # Iterate over the languages
        for language in languages:
            # Get ocrdata 
            ocrdata = ocrkit.get_ocr_data(delete_minus1_confidences=False, tiff_image=tiff_image, language=language)
            # Get Evaluation Data
            evaluation_ocrdata = utils.evaluate_ocrdata(ocrdata)
            # Save evaluation data to Excel
            evaluation_ocrdata.to_excel(os.path.join(file_output_folder, f"evaluation_ocrdata_{language}.xlsx"))
            # Create searchable PDF
            ocrkit.create_searchable_pdf(
                tiff_image=tiff_image,
                out_filename=os.path.join(file_output_folder, f"tiff_image_{language}.pdf"),
                language="{}".format(language),
            )

