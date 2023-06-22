import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import pytesseract




# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-02.pdf")
tiff_image = inputpdf.convert_to_tiff_with_ghostscript()
osd_data = pytesseract.image_to_osd(tiff_image.path)
print(osd_data)

"""
# Convert to Tiff Image
tiff_image = tiff_image.binarize_adaptive_threshold()
tiff_image = tiff_image.despeckle()
tiff_image.save_image("outputfolder/adaptive_sharpen1.tiff")

tiff_image = tiff_image.binarize_adaptive_threshold()
tiffimage = tiff_image.despeckle()
tiff_image.save_image("outputfolder/adaptive_sharpen2.tiff")

tiff_image = tiff_image.binarize_adaptive_threshold()
tiff_image = tiff_image.despeckle()
tiff_image.save_image("outputfolder/adaptive_sharpen3.tiff")
"""