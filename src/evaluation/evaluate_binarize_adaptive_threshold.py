import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit
import utils


# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-06.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()


# Preprocessing
tiff_image_preprocessed = tiff_image.binarize_adaptive_threshold()

# Save
tiff_image.save_image("outputfolder/tiff_image.tiff")
tiff_image_preprocessed.save_image("outputfolder/tiff_image_preprocessed.tiff")

# Get OCRdata
tiff_image_ocr_data = ocrkit.get_ocr_data(tiff_image=tiff_image, language="deu")


tiff_image_preprocessed_ocr_data = ocrkit.get_ocr_data(
    tiff_image=tiff_image_preprocessed, language="deu"
)

utils.evaluate_preprocessing(
    ocrdata_without_preprocessing=tiff_image_ocr_data,
    ocrdata_with_preprocessing=tiff_image_preprocessed_ocr_data,
)
