import os
import pytesseract
import pandas as pd
from PIL import Image
from pytesseract import Output
from csv import QUOTE_NONE


def get_pdf_and_ocrdata(
    image: str, outputfolder: str = "tmp", language: str = "deu"
):
    file_basename = os.path.join(outputfolder, os.path.basename(image))
    ocrdata = pytesseract.pytesseract.run_tesseract(
        input_filename=image,
        output_filename_base=file_basename,
        lang=language,
        extension="pdf",
        config="tsv",
    )
    pdf = file_basename + ".pdf"
    tsv = file_basename + ".tsv"
    ocrdata = pd.read_csv(tsv, delimiter="\t", quoting=QUOTE_NONE)
    # Remove all rows with confidence = -1, Words with confidence -1 wont be written to pdf
    ocrdata = ocrdata[ocrdata["conf"] != -1]

    return pdf, ocrdata


def get_average_confidence(ocrdata: pd.DataFrame, page_number: int = None):
    average_confidence = ocrdata["conf"].mean()
    return average_confidence


def get_number_of_detected_words(ocrdata: pd.DataFrame, page_number: int = None):
    number_of_detected_words = ocrdata["conf"].count()
    return number_of_detected_words


def get_variance_of_confidence(ocrdata: pd.DataFrame, page_number: int = None):
    variance_of_confidence = ocrdata["conf"].var()
    return variance_of_confidence


def get_minimum_of_confidence(ocrdata: pd.DataFrame, page_number: int = None):
    minimum_of_confidence = ocrdata["conf"].min()
    return minimum_of_confidence


def get_maximum_of_confidence(ocrdata: pd.DataFrame, page_number: int = None):
    maximum_of_confidence = ocrdata["conf"].max()
    return maximum_of_confidence


def evaluate_ocrdata(ocrdata: pd.DataFrame):
    ocr_evaluation = pd.DataFrame(
        columns=[
            "Page",
            "average_confidence",
            "number_of_detected_words",
            "variance_of_confidence",
            "minimum_of_confidence",
            "maximum_of_confidence",
        ]
    )

    page_numbers = list(ocrdata["page_num"].unique())
    page_numbers.append("Whole Document")
    for page in page_numbers:
        if page != "Whole Document":
            ocrdata_per_page = ocrdata[ocrdata["page_num"] == page]
        else:
            ocrdata_per_page = ocrdata

        # Get Statistic Values per page
        average_confidence = get_average_confidence(ocrdata_per_page)
        number_of_detected_words = get_number_of_detected_words(ocrdata_per_page)
        variance_of_confidence = get_variance_of_confidence(ocrdata_per_page)
        minimum_of_confidence = get_minimum_of_confidence(ocrdata_per_page)
        maximum_of_confidence = get_maximum_of_confidence(ocrdata_per_page)

        # Create new row
        new_row = {
            "Page": page,
            "average_confidence": average_confidence,
            "number_of_detected_words": number_of_detected_words,
            "variance_of_confidence": variance_of_confidence,
            "minimum_of_confidence": minimum_of_confidence,
            "maximum_of_confidence": maximum_of_confidence,
        }

        # Append row to dataframe
        new_row = pd.DataFrame(new_row, index=[page])
        ocr_evaluation = pd.concat([ocr_evaluation, new_row], axis=0, ignore_index=True)

    return ocr_evaluation

def evaluate_preprocessing(image_without_preprocessing,image_with_preprocessing, language = "deu"):
    pdf_without_preprocessing, ocrdata_without_preprocessing = get_pdf_and_ocrdata(image=image_without_preprocessing, outputfolder="tmp", language=language)
    ocr_evaluation_without_preprocessing = evaluate_ocrdata(ocrdata_without_preprocessing)

    pdf_with_preprocessing, ocrdata_with_preprocessing = get_pdf_and_ocrdata(image=image_with_preprocessing, outputfolder="tmp", language=language)
    ocr_evaluation_with_preprocessing = evaluate_ocrdata(ocrdata_with_preprocessing)

    return pdf_without_preprocessing, pdf_with_preprocessing, ocr_evaluation_without_preprocessing, ocr_evaluation_with_preprocessing

