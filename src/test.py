import sys

from ocrkit import *
import ocrkit
import sys


# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/OCRTestDocument.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff_with_ghostscript()
tiff_image_bin = tiff_image.binarize_adaptive_threshold()
tiff_image_bin.save_image("MyTest.tiff")

# Get OCRDATA
ocrdatadeutsch = ocrkit.get_ocr_data(
    tiff_image=tiff_image, language="deu"
)
print(ocrdatadeutsch)
