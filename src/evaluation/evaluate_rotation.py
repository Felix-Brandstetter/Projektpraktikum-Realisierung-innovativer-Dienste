import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit
import utils


# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/OCRTestDocument.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()


# Preprocessing
tiff_image_preprocessed = tiff_image.rotate_image_to_corrected_text_orientation()


tiff_image_preprocessed.save_image("outputfolder/tiff_image_preprocessed.tiff")

# Get OCRdata
tiff_image_ocr_data = ocrkit.get_ocr_data(tiff_image=tiff_image, language="deu+eng+chi_sim")


tiff_image_preprocessed_ocr_data = ocrkit.get_ocr_data(
    tiff_image=tiff_image_preprocessed, language="deu+eng+chi_sim"
)


evaluation_without_preprocessing = utils.evaluate_ocrdata(tiff_image_ocr_data)
evaluation_with_preprocessing = utils.evaluate_ocrdata(tiff_image_preprocessed_ocr_data)


evaluation_without_preprocessing.to_excel("evaluation_without_preprocessing.xlsx")
evaluation_with_preprocessing.to_excel("evaluation_with_preprocessing.xlsx")