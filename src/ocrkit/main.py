import preprocessing
import ocr
import evaluation

# create comparison image and preprocessed image
tiff = preprocessing.convert_to_tiff(
    "/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-09.pdf", "tmp"
)
binary_tiff = preprocessing.convert_to_binary_tiff(
    "/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-09.pdf", "tmp"
)


# Create hocr file and ocrdata for each image
(
    hocr_without_preprocessing,
    ocrdata_without_preprocessing,
) = ocr.create_hocr_file_and_ocrdata_from_tiff_image(
    image=tiff, outputfolder="tmp", language="eng"
)


(
    hocr_with_preprocessing,
    ocrdata_with_preprocessing,
) = ocr.create_hocr_file_and_ocrdata_from_tiff_image(
    image=binary_tiff, outputfolder="tmp", language="eng"
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
ocr.create_ocr_pdf_from_hocr_file(
    hocr_filename=hocr_without_preprocessing,
    tiff_image=tiff,
    out_filename="tmp/pdf_without_preprocessing.pdf",
    fontcolor="red",
    invisible_text=False,
)

ocr.create_ocr_pdf_from_hocr_file(
    hocr_filename=hocr_with_preprocessing,
    tiff_image=binary_tiff,
    out_filename="tmp/pdf_with_preprocessing.pdf",
    fontcolor="red",
    invisible_text=False,
)
