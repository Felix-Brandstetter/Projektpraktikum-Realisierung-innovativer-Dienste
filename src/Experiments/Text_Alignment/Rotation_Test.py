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

## Test the impact of different rotation angles on OCR results

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000

# Create the path for the output folder where the results are saved
output_folder = "/RIDSS2023/Experiments_Results/Text_Alignment/Rotation_Test"
# Check if the output folder already exists and delete it if it does
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
# Create the output folder
os.makedirs(output_folder)

# Path to the input folder with PDFs with correct rotation
pdfs_with_correct_rotation = os.listdir("/RIDSS2023/src/Experiments/Test_Files/Correct_Rotation_PDFs")

# Path to the input folder with PDFs with wrong rotation
pdfs_with_wrong_rotation = os.listdir("/RIDSS2023/src/Experiments/Test_Files/Wrong_Rotation_PDFs")

# Check if the number of files in both folders is the same
if len(pdfs_with_correct_rotation) == len(pdfs_with_wrong_rotation):
    # Iterate over the files in both folders simultaneously
    for pdf_correct_rotated, pdf_wrong_rotated in zip(pdfs_with_correct_rotation, pdfs_with_wrong_rotation):
        path_to_pdf_correct_rotated = os.path.join("/RIDSS2023/src/Experiments/Test_Files/Correct_Rotation_PDFs", pdf_correct_rotated)
        path_to_pdf_wrong_rotated = os.path.join("/RIDSS2023/src/Experiments/Test_Files/Wrong_Rotation_PDFs", pdf_wrong_rotated)

        # Generate the output path for the current file
        file_output_folder = os.path.join(output_folder, pdf_correct_rotated[:-4])

        # Delete the output folder if it already exists
        if os.path.exists(file_output_folder):
            shutil.rmtree(file_output_folder)

        # Create the output folder
        os.makedirs(file_output_folder)

        # Create a new InputPDF object for the PDF with correct rotation
        pdf_correct_rotated = InputPDF(path_to_pdf_correct_rotated)

        # Create a new InputPDF object for the PDF with wrong rotation
        pdf_wrong_rotated = InputPDF(path_to_pdf_wrong_rotated)

        # Convert the PDF with correct rotation to a TIFF image using Ghostscript
        tiff_image_correct_rotated = pdf_correct_rotated.convert_to_tiff_with_ghostscript(dpi=300)

        # Convert the PDF with wrong rotation to a TIFF image using Ghostscript
        tiff_image_wrong_rotated = pdf_wrong_rotated.convert_to_tiff_with_ghostscript(dpi=300)

        # Extract OCR data from the TIFF image of the PDF with correct rotation
        ocrdata_tiff_image_correct_rotated = ocrkit.get_ocr_data(tiff_image=tiff_image_correct_rotated, language="deu+eng+chi_sim")

        # Extract OCR data from the TIFF image of the PDF with wrong rotation
        ocrdata_tiff_image_wrong_rotated = ocrkit.get_ocr_data(tiff_image=tiff_image_wrong_rotated, language="deu+eng+chi_sim")

        # Evaluate the OCR data for the PDF with correct rotation
        evaluation_ocrdata_tiff_image_correct_rotated = utils.evaluate_ocrdata(ocrdata_tiff_image_correct_rotated)

        # Evaluate the OCR data for the PDF with wrong rotation
        evaluation_ocrdata_tiff_image_wrong_rotated = utils.evaluate_ocrdata(ocrdata_tiff_image_wrong_rotated)

        # Save the evaluation results as Excel files
        evaluation_ocrdata_tiff_image_correct_rotated.to_excel(os.path.join(file_output_folder, "evaluation_ocrdata_correct_orientation.xlsx"))
        evaluation_ocrdata_tiff_image_wrong_rotated.to_excel(os.path.join(file_output_folder, "evaluation_ocrdata_wrong_orientation.xlsx"))

        # Create a searchable PDF from the TIFF image of the PDF with correct rotation
        ocrkit.create_searchable_pdf(tiff_image=tiff_image_correct_rotated, out_filename=os.path.join(file_output_folder, f"tiff_image_correct_rotated.pdf"), language="deu+eng+chi_sim")

        # Create a searchable PDF from the TIFF image of the PDF with wrong rotation
        ocrkit.create_searchable_pdf(tiff_image=tiff_image_wrong_rotated, out_filename=os.path.join(file_output_folder, f"tiff_image_wrong_rotated.pdf"), language="deu+eng+chi_sim")

else:
    print("Folders must have the same length")
