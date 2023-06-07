import pandas as pd

import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit

#Get the middle point of the bounding box of a word of a OCR DataFrame
def get_middle_point(ocrdata_per_page, index):
    row = ocrdata_per_page.iloc(index)
    middle_point = []
    middle_point_x = row["left"] + 0.5 * row["width"]
    middle_point.append(middle_point_x)
    middle_point_y = row["top"] + 0.5 * row["height"]
    middle_point.append(middle_point_y)
    return middle_point

#Calculate which middle point out of a list of middle points is closest to a certain middle point
def closest_middle_points(
      ocrdata_without_preprocessing_per_page, ocrdata_with_preprocessing, index1, indexes_middle_points
):
      middle_point_row1 = get_middle_point(ocrdata_without_preprocessing_per_page, index1)
      middle_point_row1_x = middle_point_row1[0] 
      middle_point_row1_y = middle_point_row1[1]
      euclidian_distances = []
      for i in range(len(indexes_middle_points)):
          middle_point_row2 = get_middle_point(ocrdata_with_preprocessing, indexes_middle_points[i])
          middle_point_row2_x = middle_point_row2[0]
          middle_point_row2_y = middle_point_row2[1]
          euclidian_distance_middle_points = ((middle_point_row2_x-middle_point_row1_x)^2 + (middle_point_row2_y-middle_point_row1_y)^2)^0.5  
          euclidian_distances.append(euclidian_distance_middle_points)
        
      min_distance = min(euclidian_distances)
      min_distance_index = euclidian_distances.index(min_distance)         
        
      return indexes_middle_points[min_distance_index]

#Append a new row to the DataFrame of the Evaluation Comparison 
def append_row(
    ocrdata_without_preprocessing_per_page: pd.DataFrame,
    ocrdata_with_preprocessing_per_page: pd.DataFrame,
    ocr_evaluation_comparison,
    index1, 
    index2, 
    page
):
    row1 = ocrdata_without_preprocessing_per_page.iloc(index1)
    row2 = ocrdata_with_preprocessing_per_page.iloc(index2)
    row1_confidence = row1["conf"]
    row2_confidence = row2["conf"]
    row1_text = row1["text"]
    row2_text = row2["text"]
    differnce_confidence = row2_confidence - row1_confidence
    if(row1_confidence != 0):
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
        "text1": row1_text, 
        "text2": row2_text,
        }
    # Append row to dataframe
    new_row = pd.DataFrame(new_row, index=[page])
    ocr_evaluation_comparison = pd.concat(
        [ocr_evaluation_comparison, new_row], axis=0, ignore_index=True
        )               

      
#The confidence of each word in the DataFrame before preprocessing and after preprocesing are compared
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
            "text1"
            "text2"
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
            count_middle_points = 0 #counts the middle points of row2 that are in a bounding box of row1
            indexes_middle_points = []  #list that holds the indexes of the middle points of row2, that are in the bounding box of row1
            for index2, row2 in ocrdata_with_preprocessing_per_page.iterrows(): 
                middle_point_row2 = get_middle_point(ocrdata_with_preprocessing_per_page, index2)
                middle_point_row2_x = middle_point_row2[0]
                middle_point_row2_y = middle_point_row2[1] 
                if (
                    middle_point_row2_x >=  row1["left"]
                    and middle_point_row2_x <=  (row1["left"] + row1["width"])
                    and middle_point_row2_y >=  row1["top"]
                    and middle_point_row2_y <=  (row1["top"] + row1["height"])
                ):
                   count_middle_points += 1
                   indexes_middle_points.append(index2)
            if count_middle_points == 1:
                append_row(ocrdata_without_preprocessing_per_page, ocrdata_with_preprocessing_per_page, ocr_evaluation_comparison, index1, indexes_middle_points[0], page)
            elif count_middle_points >= 2:
                closest_middle_point = closest_middle_points(ocrdata_without_preprocessing_per_page, ocrdata_with_preprocessing, index1, indexes_middle_points)
                append_row(ocrdata_without_preprocessing_per_page, ocrdata_with_preprocessing_per_page, ocr_evaluation_comparison, index1, closest_middle_point, page) 
    
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

ocr_evaluation_comparison.to_Excel("test_comparison.xlsx")

#TODO Summe der Confidencen
#TODO Center Punkte der Bounding Box vergleichen
#TODO PDF aus verschiedenen Dokumneten zusammenbauen
