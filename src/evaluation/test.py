import sys
import utils
sys.path.append("/RIDSS2023/src")
import ocrkit


# Create new Inputfile
inputpdf = ocrkit.InputPDF("/RIDSS2023/inputfolder/ToOcr-06.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()
ocrdata = ocrkit.get_ocr_data(tiff_image=tiff_image, language="deu")
utils.plot_confidences(ocrdata=ocrdata)