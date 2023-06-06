import pandas as pd

import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit


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
        for index1, row1 in ocrdata_without_preprocessing_per_page.iterrows():
            #print(row1)
            #print(ocrdata_with_preprocessing_per_page.loc[[index1]])
            for index2, row2 in ocrdata_with_preprocessing_per_page.iterrows():
                if (
                    row1["left"] == row2["left"]
                    and row1["top"] == row2["top"]
                    and row1["width"] == row2["width"]
                    and row1["height"] == row2["height"]
                ):
                    row1_confidence = row1["conf"]
                    row2_confidence = row2["conf"]
                    differnce_confidence = row2_confidence - row1_confidence
                    percentage_differnce_confidence = (
                        differnce_confidence / row1_confidence
                    )
                    new_row = {
                        "Location": "location tbd",
                        "Page": page,
                        "confidence_before": row1_confidence,
                        "confidence_after": row2_confidence,
                        "differnce_in_confidence": differnce_confidence,
                        "percentage_differnce_confidence": percentage_differnce_confidence,
                    }
                    # Append row to dataframe
                    new_row = pd.DataFrame(new_row, index=[page])
                    ocr_evaluation_comparison = pd.concat(
                        [ocr_evaluation_comparison, new_row], axis=0, ignore_index=True
                    )

    print(ocr_evaluation_comparison.head())
    ocr_evaluation_comparison.to_excel("output.xlsx")
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

#TODO Summe der Confidencen
#TODO Center Punkte der Bounding Box vergleichen
#TODO PDF aus verschiedenen Dokumneten zusammenbauen
