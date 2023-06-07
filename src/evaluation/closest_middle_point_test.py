import pandas as pd
from numpy.linalg import norm
import numpy as np
import sys
from boundingbox import BoundingBox

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit


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


# Append a new row to the DataFrame of the Evaluation Comparison
def append_row(
    ocrdata_without_preprocessing_per_page: pd.DataFrame,
    ocrdata_with_preprocessing_per_page: pd.DataFrame,
    ocr_evaluation_comparison,
    index1,
    index2,
    page,
):
    row1 = ocrdata_without_preprocessing_per_page.iloc[index1]
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
    # Append row to dataframe
    new_row = pd.DataFrame(new_row, index=[page])
    ocr_evaluation_comparison = pd.concat(
        [ocr_evaluation_comparison, new_row], axis=0, ignore_index=True
    )
    return ocr_evaluation_comparison


# The confidence of each word in the DataFrame before preprocessing and after preprocesing are compared
def evaluation_comparison(
    ocrdata_without_preprocessing: pd.DataFrame,
    ocrdata_with_preprocessing: pd.DataFrame,
):
    ocr_evaluation_comparison = pd.DataFrame(
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
                if boundingbox_without_preprocessing.is_point_inside_bounding_box(
                    boundingbox_with_preprocessing.middle_point
                ):
                    list_of_bounding_boxes.append(boundingbox_with_preprocessing)
            if len(list_of_bounding_boxes) == 1:
                ocr_evaluation_comparison = append_row(
                    ocrdata_without_preprocessing_per_page,
                    ocrdata_with_preprocessing_per_page,
                    ocr_evaluation_comparison,
                    index1,
                    list_of_bounding_boxes[0].index_in_ocr_data,
                    page,
                )
            elif len(list_of_bounding_boxes) >= 2:
                closest_bounding_box = get_closest_bounding_box(
                    boundingbox_without_preprocessing, list_of_bounding_boxes
                )
                ocr_evaluation_comparison = append_row(
                    ocrdata_without_preprocessing_per_page,
                    ocrdata_with_preprocessing_per_page,
                    ocr_evaluation_comparison,
                    index1,
                    closest_bounding_box.index_in_ocr_data,
                    page,
                )

    print(ocr_evaluation_comparison.head())
    return ocr_evaluation_comparison


# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()


# Preprocessing
tiff_image_preprocessed = tiff_image.binarize_adaptive_threshold()

# Save
# tiff_image.save_image("outputfolder/tiff_image.tiff")
# tiff_image_preprocessed.save_image("outputfolder/tiff_image_preprocessed.tiff")

# Get OCRdata
tiff_image_ocr_data = ocrkit.get_ocr_data(tiff_image=tiff_image, language="deu")
print(len(tiff_image_ocr_data))

tiff_image_preprocessed_ocr_data = ocrkit.get_ocr_data(
    tiff_image=tiff_image_preprocessed, language="deu"
)
print(len(tiff_image_preprocessed_ocr_data))


ocr_evaluation_comparison = evaluation_comparison(
    ocrdata_without_preprocessing=tiff_image_ocr_data,
    ocrdata_with_preprocessing=tiff_image_preprocessed_ocr_data,
)
print(len(ocr_evaluation_comparison))

ocr_evaluation_comparison.to_excel("test_comparison.xlsx")

# TODO Summe der Confidencen
# TODO Center Punkte der Bounding Box vergleichen
# TODO PDF aus verschiedenen Dokumneten zusammenbauen
