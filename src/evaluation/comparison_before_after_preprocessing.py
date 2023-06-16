import pandas as pd
from numpy.linalg import norm
import numpy as np
import sys
from boundingbox import BoundingBox

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit
import utils 


# Get the middle point of the bounding box of a word of a OCR DataFrame
def get_closest_bounding_box(
    source_bounding_box: BoundingBox, list_of_boundingboxes: list
) -> BoundingBox:
    closest_distance = None
    closest_bounding_box = None
    for bounding_box in list_of_boundingboxes:
        distance = norm(
            np.asarray(source_bounding_box.middle_point)
            - np.asarray(bounding_box.middle_point)
        )
        if closest_distance is None:
            closest_distance = distance
            closest_bounding_box = bounding_box
        elif distance < closest_distance:
            closest_distance = distance
            closest_bounding_box = bounding_box
    return closest_bounding_box

#Create a new row of the DataFrame of the Before and After Preprocessing Comparison
def create_row(    
    ocrdata_with_preprocessing_per_page: pd.DataFrame,
    row1,
    index2,
    page,
):
    row2 = ocrdata_with_preprocessing_per_page.iloc[index2]
    row1_confidence = row1["conf"]
    row2_confidence = row2["conf"]
    row1_text = row1["text"]
    row2_text = row2["text"]
    differnce_confidence = row2_confidence - row1_confidence
    percentage_differnce_confidence = np.nan
    if row1_confidence != 0:
        percentage_differnce_confidence = differnce_confidence / row1_confidence
    new_row = {
        "Location": "location tbd",
        "Page": page,
        "confidence_before": row1_confidence,
        "confidence_after": row2_confidence,
        "differnce_in_confidence": differnce_confidence,
        "percentage_differnce_confidence": percentage_differnce_confidence,
        "text1": row1_text,
        "text2": row2_text,
    }
    return new_row

# Append a new row to the DataFrame of the Before and After Preprocessing Comparison
def append_row(
    ocrdata_comparison_before_after_preprocessing,
    new_row,
    page,
):
    # Append row to dataframe
    new_row = pd.DataFrame(new_row, index=[page])
    ocrdata_comparison_before_after_preprocessing = pd.concat(
        [ocrdata_comparison_before_after_preprocessing, new_row], axis=0, ignore_index=True
    )
    return ocrdata_comparison_before_after_preprocessing


# The confidence of each word in the DataFrame before preprocessing and after preprocesing are compared
def get_ocrdata_of_comparison_before_after_preprocessing(
    ocrdata_without_preprocessing: pd.DataFrame,
    ocrdata_with_preprocessing: pd.DataFrame,
):
    ocrdata_comparison_before_after_preprocessing = pd.DataFrame(
        columns=[
            "Location",
            "Page",
            "confidence_before",
            "confidence_after",
            "differnce_in_confidence",
            "percentage_differnce_confidence",
            "text1",
            "text2",
        ]
    )

    page_numbers = list(ocrdata_without_preprocessing["page_num"].unique())
    for page in page_numbers:
        ocrdata_without_preprocessing_per_page = ocrdata_without_preprocessing[
            ocrdata_without_preprocessing["page_num"] == page
        ]
        ocrdata_with_preprocessing_per_page = ocrdata_with_preprocessing[
            ocrdata_with_preprocessing["page_num"] == page
        ]
        for index1 in range(len(ocrdata_without_preprocessing_per_page)):
            row1 = ocrdata_without_preprocessing_per_page.iloc[index1]
            boundingbox_without_preprocessing = BoundingBox(
                top=row1["top"],
                left=row1["left"],
                width=row1["width"],
                height=row1["height"],
                index_in_ocr_data=index1,
            )
            list_of_bounding_boxes = []
            for index2 in range(len(ocrdata_with_preprocessing_per_page)):
                row2 = ocrdata_with_preprocessing_per_page.iloc[index2]
                boundingbox_with_preprocessing = BoundingBox(
                    top=row2["top"],
                    left=row2["left"],
                    width=row2["width"],
                    height=row2["height"],
                    index_in_ocr_data=index2,
                )
                if boundingbox_without_preprocessing.is_comparison_boundingbox_inside_boundingbox(
                    boundingbox_with_preprocessing
                ):
                    list_of_bounding_boxes.append(boundingbox_with_preprocessing)
            if len(list_of_bounding_boxes) == 1:
                new_row = create_row(
                    ocrdata_with_preprocessing_per_page,
                    row1,
                    list_of_bounding_boxes[0].index_in_ocr_data,
                    page,
                )
                ocrdata_comparison_before_after_preprocessing = append_row(
                    ocrdata_comparison_before_after_preprocessing,
                    new_row,
                    page,
                )
            elif len(list_of_bounding_boxes) >= 2:
                closest_bounding_box = get_closest_bounding_box(
                    boundingbox_without_preprocessing, list_of_bounding_boxes
                )
                new_row = create_row(
                    ocrdata_with_preprocessing_per_page,
                    row1,
                    closest_bounding_box.index_in_ocr_data,
                    page,
                )
                ocrdata_comparison_before_after_preprocessing = append_row(
                    ocrdata_comparison_before_after_preprocessing,
                    new_row,
                    page,
                )
            elif len(list_of_bounding_boxes) >= 0:
                print(row1["text"])

    print(ocrdata_comparison_before_after_preprocessing.head())
    return ocrdata_comparison_before_after_preprocessing

def evaluation_of_comparison(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    evaluation_of_comparison_DataFrame = pd.DataFrame(
        columns=[
            "Page",
            "Number of compared words",
            "average confidence before preprocessing",
            "average confidence after preprocessing",
            "average differnce in confidence",
            "average percentage difference in confidence",
            "minimum of confidence before preprocessing",
            "minimum of confidence of confidence after preprocessing",
            "maximum of confidence before preprocessing",
            "maximum of confidence of confidence after preprocessing",
            "maximum of differnce in confidence",
            "maximum of percentage difference in confidence",
            "sum of confidence before preprocessing",
            "sum of confidence after preprocessing",
            "standard deviation of confidence before preprocessing",
            "standard deviation of confidence after preprocessing",
            "standard deviation of differnce in confidence",
            "standard deviation of percentage difference in confidence",
            "number of confidences under 25 before preprocessing",
            "number of confidences under 25 after preprocessing",
            "number of confidences under 50 before preprocessing",
            "number of confidences under 50 after preprocessing",
        ]
    )

    page_numbers = list(evaluation_of_comparison_DataFrame["Page"].unique())
    page_numbers.append("Whole Document")
    for page in page_numbers:
        if page != "Whole Document":
            ocrdata_per_page = ocrdata_comparison_before_after_preprocessing[ocrdata_comparison_before_after_preprocessing["Page"] == page]
        else:
            ocrdata_per_page = ocrdata_comparison_before_after_preprocessing

        # Get Statistic Values per page
        number_of_compared_words = utils.get_number_of_compared_words(ocrdata_per_page)
        average_confidence_before_preprocessing = utils.get_average_confidence_before_preprocessing(ocrdata_per_page)
        average_confidence_after_preprocessing = utils.get_average_confidence_after_preprocessing(ocrdata_per_page)
        average_differnce_in_confidence = utils.get_average_differnce_in_confidence(ocrdata_per_page)
        average_percentage_difference_in_confidence = utils.get_average_percentage_differnce_in_confidence(ocrdata_per_page)
        minimum_of_confidence_before_preprocessing = utils.get_minimum_of_confidence_before_preprocessing(ocrdata_per_page)
        minimum_of_confidence_of_confidence_after_preprocessing = utils.get_minimum_of_confidence_after_preprocessing(ocrdata_per_page)
        maximum_of_confidence_before_preprocessin = utils.get_maximum_of_confidence_before_preprocessing(ocrdata_per_page)
        maximum_of_confidence_of_confidence_after_preprocessing = utils.get_maximum_of_confidence_after_preprocessing(ocrdata_per_page)
        maximum_of_differnce_in_confidence = utils.get_maximum_of_differnce_in_confidence(ocrdata_per_page)
        maximum_of_percentage_difference_in_confidence = utils.get_maximum_of_percentage_differnce_in_confidence(ocrdata_per_page)
        sum_of_confidence_before_preprocessing = utils.get_sum_of_confidence_before_preprocessing(ocrdata_per_page)
        sum_of_confidence_after_preprocessing = utils.get_sum_of_confidence_after_preprocessing(ocrdata_per_page)
        standard_deviation_of_confidence_before_preprocessing = utils.get_standard_deviation_of_confidence_before_preprocessing(ocrdata_per_page)
        standard_deviation_of_confidence_after_preprocessing = utils.get_standard_deviation_of_confidence_after_preprocessing(ocrdata_per_page)
        standard_deviation_of_differnce_in_confidence = utils.get_standard_deviation_of_differnce_in_confidence(ocrdata_per_page)
        standard_deviation_of_percentage_difference_in_confidence = utils.get_standard_deviation_of_percentage_differnce_in_confidence(ocrdata_per_page)
        number_of_confidences_under_25_before_preprocessing = utils.get_number_of_confidences_under_25_before_preprocessing(ocrdata_per_page)
        number_of_confidences_under_25_after_preprocessing = utils.get_number_of_confidences_under_25_after_preprocessing(ocrdata_per_page)
        number_of_confidences_under_50_before_preprocessing = utils.get_number_of_confidences_under_50_before_preprocessing(ocrdata_per_page)
        number_of_confidences_under_50_after_preprocessing = utils.get_number_of_confidences_under_50_after_preprocessing(ocrdata_per_page)
 
        # Create new row
        new_row = {
            "Page": page,
            "Number of compared words": number_of_compared_words,
            "average confidence before preprocessing": average_confidence_before_preprocessing,
            "average confidence after preprocessing": average_confidence_after_preprocessing,
            "average differnce in confidence": average_differnce_in_confidence,
            "average percentage difference in confidence": average_percentage_difference_in_confidence,
            "minimum of confidence before preprocessing": minimum_of_confidence_before_preprocessing,
            "minimum of confidence of confidence after preprocessing": minimum_of_confidence_of_confidence_after_preprocessing,
            "maximum of confidence before preprocessing": maximum_of_confidence_before_preprocessin,
            "maximum of confidence of confidence after preprocessing": maximum_of_confidence_of_confidence_after_preprocessing,
            "maximum of differnce in confidence": maximum_of_differnce_in_confidence,
            "maximum of percentage difference in confidence": maximum_of_percentage_difference_in_confidence,
            "sum of confidence before preprocessing": sum_of_confidence_before_preprocessing,
            "sum of confidence after preprocessing": sum_of_confidence_after_preprocessing,
            "standard deviation of confidence before preprocessing": standard_deviation_of_confidence_before_preprocessing,
            "standard deviation of confidence after preprocessing": standard_deviation_of_confidence_after_preprocessing,
            "standard deviation of differnce in confidence": standard_deviation_of_differnce_in_confidence,
            "standard deviation of percentage difference in confidence": standard_deviation_of_percentage_difference_in_confidence,
            "number of confidences under 25 before preprocessing": number_of_confidences_under_25_before_preprocessing,
            "number of confidences under 25 after preprocessing": number_of_confidences_under_25_after_preprocessing,
            "number of confidences under 50 before preprocessing": number_of_confidences_under_50_before_preprocessing,
            "number of confidences under 50 after preprocessing": number_of_confidences_under_50_after_preprocessing,
        }

        # Append row to dataframe
        new_row = pd.DataFrame(new_row, index=[page])
        evaluation_of_comparison_DataFrame = pd.concat([evaluation_of_comparison_DataFrame, new_row], axis=0, ignore_index=True)

    print(evaluation_of_comparison_DataFrame)
    return evaluation_of_comparison_DataFrame










# Create new InputPDF
inputpdf = InputPDF("inputfolder/ToOcr_Seiten.pdf/ToOcr-06.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()


# Preprocessing
tiff_image_preprocessed = tiff_image.binarize_adaptive_threshold()

# Save and Create Searchable PDF
tiff_image.save_image("outputfolder/tiff_image.tiff")
tiff_image_preprocessed.save_image("outputfolder/tiff_image_preprocessed.tiff")

ocrkit.create_searchable_pdf(
    tiff_image=tiff_image,
    out_filename="outputfolder/test.pdf",
    language="deu",
    show_bounding_boxes=True,
)

ocrkit.create_searchable_pdf(
    tiff_image=tiff_image_preprocessed,
    out_filename="outputfolder/test_preprocessed.pdf",
    language="deu",
    show_bounding_boxes=True,
)

# Get ocrdata_comparison_before_after_preprocessing
tiff_image_ocr_data = ocrkit.get_ocr_data(tiff_image=tiff_image, language="deu")
print(len(tiff_image_ocr_data))

tiff_image_preprocessed_ocr_data = ocrkit.get_ocr_data(
    tiff_image=tiff_image_preprocessed, language="deu"
)
print(len(tiff_image_preprocessed_ocr_data))

#Create the DataFrame that compares the OCR Data before and after preprocessing
ocrdata_comparison_before_after_preprocessing = get_ocrdata_of_comparison_before_after_preprocessing(
    ocrdata_without_preprocessing=tiff_image_ocr_data,
    ocrdata_with_preprocessing=tiff_image_preprocessed_ocr_data,
)
print(len(ocrdata_comparison_before_after_preprocessing))
ocrdata_comparison_before_after_preprocessing.to_excel("test_comparison.xlsx")

#Create the DataFrame that evaluates the data of the comparison DataFrame
evaluation_of_comparison_DataFrame = evaluation_of_comparison(ocrdata_comparison_before_after_preprocessing)
evaluation_of_comparison_DataFrame.to_excel("test_comparison_evaluation.xlsx")

# TODO Summe der Confidencen
# TODO Center Punkte der Bounding Box vergleichen
# TODO PDF aus verschiedenen Dokumneten zusammenbauen
