import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit
import utils
import sys
import pytesseract
from pytesseract import Output

# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/OCRTestDocument.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff_with_ghostscript()
tiff_image.save_image("/RIDSS2023/outputfolder/OCRTestDocument.tiff")

# Get OCRDATA
ocrdatadeutsch = ocrkit.get_ocr_data(
    tiff_image=tiff_image, language="deu"
)
print(ocrdatadeutsch)
sys.exit(1)

ocrdataenglisch = ocrkit.get_ocr_data(
    tiff_image=tiff_image, language="eng"
)
ocrdatachi_sim = ocrkit.get_ocr_data(
    tiff_image=tiff_image, language="chi_sim"
)
ocrdatachi_all_languages= ocrkit.get_ocr_data(
    tiff_image=tiff_image, language="deu+eng+chi_sim"
)

evaluation_ocrdatadeutsch = utils.evaluate_ocrdata(ocrdatadeutsch)
evaluation_ocrdataenglisch = utils.evaluate_ocrdata(ocrdataenglisch)
evaluation_ocrdatachi_sim = utils.evaluate_ocrdata(ocrdatachi_sim)
evaluation_ocrdata_all_languages = utils.evaluate_ocrdata(ocrdatachi_all_languages)


evaluation_ocrdatadeutsch.to_excel("evaluation_ocrdatadeutsch.xlsx")
evaluation_ocrdataenglisch.to_excel("evaluation_ocrdataenglisch.xlsx")
evaluation_ocrdatachi_sim.to_excel("evaluation_ocrdatachi_sim.xlsx")
evaluation_ocrdata_all_languages.to_excel("evaluation_ocrdata_all_languages.xlsx")