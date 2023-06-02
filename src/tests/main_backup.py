import ocrkit
import tests.evaluation as evaluation

input_pdf = "/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-09.pdf"

# create comparison image and preprocessed image
original_tiff_image = ocrkit.convert_to_tiff(
    pdf=input_pdf, output_folder="tmp")

preprocessed_tiff_image = ocrkit.utils.convert_to_binary_tiff_with_adaptive_threshold(
    pdf=input_pdf, output_folder="tmp"
)


# Create hocr file and ocrdata for each image
(
    hocr_without_preprocessing,
    ocrdata_without_preprocessing,
) = ocrkit.create_hocr_file_and_ocrdata_from_tiff_image(
    image=original_tiff_image, outputfolder="tmp", language="eng"
)


(
    hocr_with_preprocessing,
    ocrdata_with_preprocessing,
) = ocrkit.create_hocr_file_and_ocrdata_from_tiff_image(
    image=preprocessed_tiff_image, outputfolder="tmp", language="eng"
)


# Evaluate original image and preporcessed image
(
    ocr_evaluation_without_preprocessing,
    ocr_evaluation_with_preprocessing,
) = evaluation.evaluate_preprocessing(
    ocrdata_without_preprocessing=ocrdata_without_preprocessing,
    ocrdata_with_preprocessing=ocrdata_with_preprocessing,
)

# Print evaluation
print(ocr_evaluation_without_preprocessing)
print(ocr_evaluation_with_preprocessing)


# Create pdf file with integrated Text
ocrkit.create_ocr_pdf_from_hocr_file(
    hocr_filename=hocr_without_preprocessing,
    tiff_image=original_tiff_image,
    out_filename="tmp/pdf_without_preprocessing.pdf",
    fontcolor="red",
    invisible_text=False,
)

ocrkit.create_ocr_pdf_from_hocr_file(
    hocr_filename=hocr_with_preprocessing,
    tiff_image=preprocessed_tiff_image,
    out_filename="tmp/pdf_with_preprocessing.pdf",
    fontcolor="red",
    invisible_text=False,
)
