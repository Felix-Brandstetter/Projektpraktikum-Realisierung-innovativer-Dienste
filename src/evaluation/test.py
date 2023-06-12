import sys
import utils
sys.path.append("/RIDSS2023/src")
import ocrkit


# Create new Inputfile
inputpdf = ocrkit.InputPDF("/RIDSS2023/src/tests/test_ressources/test_rotate_image_to_corrected_text_orientation/test_image.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()
ocrdata = ocrkit.get_ocr_data(tiff_image=tiff_image, language="deu")
utils.plot_confidences(ocrdata=ocrdata)

#TODO Plot difference in one histogramm