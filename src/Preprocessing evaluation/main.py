import preprocessing
import utils

tiff = preprocessing.convert_to_tiff("/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-09.pdf", "tmp")
binary_tiff = preprocessing.convert_to_binary_tiff( "/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-09.pdf", "tmp")

(
    pdf_without_preprocessing,
    pdf_with_preprocessing,
    ocr_evaluation_without_preprocessing,
    ocr_evaluation_with_preprocessing,
) = utils.evaluate_preprocessing(
    image_without_preprocessing=tiff,
    image_with_preprocessing=binary_tiff,
    language="deu",
)

print(ocr_evaluation_without_preprocessing)
print(ocr_evaluation_with_preprocessing)
