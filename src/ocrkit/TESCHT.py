import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *


inputpdf = InputPDF("/RIDSS2023/inputfolder/ToOcr-12.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()

#tiff_image.detect_language()
#tiff_image.detect_language2()
#tiff_image.detect_language3()


