import sys
import utils
sys.path.append("/RIDSS2023/src")
import ocrkit
from datetime import datetime


# Create new Inputfile
inputpdf = ocrkit.InputPDF("/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-20.pdf")


# Convert to Tiff Image
startTime = datetime.now()
tiff_image = inputpdf.convert_to_tiff_with_ghostscript(dpi=2400)
runtime = datetime.now() - startTime
print(runtime)
tiff_image.save_image("Test.tiff")

# Convert to Tiff Image
startTime = datetime.now()
tiff_image = inputpdf.convert_to_tiff_with_imagemagick(dpi=2400, width=2480, height=3508)
runtime = datetime.now() - startTime
print(runtime)
tiff_image.save_image("Test1.tiff")
