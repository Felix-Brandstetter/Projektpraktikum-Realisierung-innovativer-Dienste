import pandas as pd
from numpy.linalg import norm
import numpy as np
import sys
from boundingbox import BoundingBox
import matplotlib as plt

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit
import utils 


## This file contains functions for a word-by-word comparison of the OCR results before and after preprocessing


def get_closest_bounding_box(source_bounding_box: BoundingBox, list_of_boundingboxes: list) -> BoundingBox:
    """ Get the closest boundingbox to a source boundingbox out of a list of boundingboxes"""

    # Initialize variables to track the boundingbox and its distance
    closest_distance = None
    closest_bounding_box = None

    # Iterate over each bounding box in the list
    for bounding_box in list_of_boundingboxes:
        # Calculate the distance between the middle points of the source and current boundingbox
        distance = norm(
            np.asarray(source_bounding_box.middle_point)
            - np.asarray(bounding_box.middle_point)
        )
        # Update the closest distance if the distance calculated is smaller than the current closest distance,
        # and save the corresponding boundingbox as the closest boundingbox
        if closest_distance is None:
            closest_distance = distance
            closest_bounding_box = bounding_box
        elif distance < closest_distance:
            closest_distance = distance
            closest_bounding_box = bounding_box

    return closest_bounding_box

def create_row(    
    ocrdata_with_preprocessing_per_page: pd.DataFrame,
    row1,
    index2,
    page,
):
    """Create a new row for the ocrdata_comparison_before_after_preprocessing DataFrame"""

    # Get the row from ocrdata_with_preprocessing_per_page at the given index
    row2 = ocrdata_with_preprocessing_per_page.iloc[index2]

    # Extract the necessary information from the rows
    row1_confidence = row1["conf"]
    row2_confidence = row2["conf"]
    row1_text = row1["text"]
    row2_text = row2["text"]

    # Calculate the difference in confidence between row2 and row1
    difference_confidence = row2_confidence - row1_confidence

    # Calculate the percentage difference in confidence if row1_confidence is not zero
    percentage_difference_confidence = np.nan
    if row1_confidence != 0:
        percentage_difference_confidence = difference_confidence / row1_confidence

    # Create a new row dictionary with the extracted information
    new_row = {
        "Location": "location tbd",
        "Page": page,
        "confidence_before": row1_confidence,
        "confidence_after": row2_confidence,
        "difference_in_confidence": difference_confidence,
        "percentage_difference_confidence": percentage_difference_confidence,
        "text1": row1_text,
        "text2": row2_text,
    }
    return new_row

def append_row(
    ocrdata_comparison_before_after_preprocessing,
    new_row,
    page,
):
    """ Append a new row to the ocrdata_comparison_before_after_preprocessing DataFrame"""

    # Convert the new_row dictionary to a DataFrame with the given page as the index
    new_row = pd.DataFrame(new_row, index=[page])

    # Concatenate the new_row DataFrame to the ocrdata_comparison_before_after_preprocessing DataFrame
    ocrdata_comparison_before_after_preprocessing = pd.concat(
        [ocrdata_comparison_before_after_preprocessing, new_row], axis=0, ignore_index=True
    )

    # Return the updated ocrdata_comparison_before_after_preprocessing DataFrame
    return ocrdata_comparison_before_after_preprocessing



def get_ocrdata_of_comparison_before_after_preprocessing(
    ocrdata_without_preprocessing: pd.DataFrame,
    ocrdata_with_preprocessing: pd.DataFrame,
):
    """ The OCR-Data of each word before and after preprocessing is compared"""
    
    # Create an empty DataFrame to store the comparison results and 
    # set the column titles for all the statistics to be values to be included in the DataFrame
    ocrdata_comparison_before_after_preprocessing = pd.DataFrame(
        columns=[
            "Location",
            "Page",
            "confidence_before",
            "confidence_after",
            "difference_in_confidence",
            "percentage_difference_confidence",
            "text1",
            "text2",
        ]
    )

    # Get the unique page numbers from the ocrdata_without_preprocessing DataFrame
    page_numbers = list(ocrdata_without_preprocessing["page_num"].unique())

    # Iterate over each page number
    for page in page_numbers:
        # Filter the ocrdata_without_preprocessing DataFrame for the current page
        ocrdata_without_preprocessing_per_page = ocrdata_without_preprocessing[
            ocrdata_without_preprocessing["page_num"] == page
        ]

        # Filter the ocrdata_with_preprocessing DataFrame for the current page
        ocrdata_with_preprocessing_per_page = ocrdata_with_preprocessing[
            ocrdata_with_preprocessing["page_num"] == page
        ]

        # Iterate over each row in ocrdata_without_preprocessing_per_page
        for index1 in range(len(ocrdata_without_preprocessing_per_page)):
            # Get the current row from ocrdata_without_preprocessing_per_page
            row1 = ocrdata_without_preprocessing_per_page.iloc[index1]

            # Create a BoundingBox object for the current row in ocrdata_without_preprocessing_per_page
            boundingbox_without_preprocessing = BoundingBox(
                top=row1["top"],
                left=row1["left"],
                width=row1["width"],
                height=row1["height"],
                index_in_ocr_data=index1,
            )

            # Create an empty list to store the bounding boxes from ocrdata_with_preprocessing_per_page
            list_of_bounding_boxes = []

            # Iterate over each row in ocrdata_with_preprocessing_per_page
            for index2 in range(len(ocrdata_with_preprocessing_per_page)):
                # Get the current row from ocrdata_with_preprocessing_per_page
                row2 = ocrdata_with_preprocessing_per_page.iloc[index2]

                # Create a BoundingBox object for the current row in ocrdata_with_preprocessing_per_page
                boundingbox_with_preprocessing = BoundingBox(
                    top=row2["top"],
                    left=row2["left"],
                    width=row2["width"],
                    height=row2["height"],
                    index_in_ocr_data=index2,
                )

                # Check if the bounding box from ocrdata_with_preprocessing_per_page is inside the bounding box from ocrdata_without_preprocessing_per_page
                if boundingbox_without_preprocessing.is_comparison_boundingbox_inside_boundingbox(
                    boundingbox_with_preprocessing
                ):
                    # If the condition is met, add the bounding box to the list_of_bounding_boxes
                    list_of_bounding_boxes.append(boundingbox_with_preprocessing)

            # Compare the number of bounding boxes found
            if len(list_of_bounding_boxes) == 1:
                # If only one bounding box is found, create a row using the create_row function
                new_row = create_row(
                    ocrdata_with_preprocessing_per_page,
                    row1,
                    list_of_bounding_boxes[0].index_in_ocr_data,
                    page,
                )
                # Append the new row to the ocrdata_comparison_before_after_preprocessing DataFrame using the append_row function
                ocrdata_comparison_before_after_preprocessing = append_row(
                    ocrdata_comparison_before_after_preprocessing,
                    new_row,
                    page,
                )
            elif len(list_of_bounding_boxes) >= 2:
                # If multiple bounding boxes are found, get the closest bounding box using the get_closest_bounding_box function
                closest_bounding_box = get_closest_bounding_box(
                    boundingbox_without_preprocessing, list_of_bounding_boxes
                )
                # Create a row using the create_row function with the closest bounding box
                new_row = create_row(
                    ocrdata_with_preprocessing_per_page,
                    row1,
                    closest_bounding_box.index_in_ocr_data,
                    page,
                )
                # Append the new row to the ocrdata_comparison_before_after_preprocessing DataFrame using the append_row function
                ocrdata_comparison_before_after_preprocessing = append_row(
                    ocrdata_comparison_before_after_preprocessing,
                    new_row,
                    page,
                )

    # Return the ocrdata_comparison_before_after_preprocessing DataFrame
    return ocrdata_comparison_before_after_preprocessing


def evaluation_of_comparison(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """ Evaluate the comparison data"""

    # Create an empty DataFrame to store the evaluation results
    evaluation_of_comparison_DataFrame = pd.DataFrame(
        columns=[
            "Page",
            "Number of compared words",
            "average confidence before preprocessing",
            "average confidence after preprocessing",
            "average difference in confidence",
            "average percentage difference in confidence",
            "minimum of confidence before preprocessing",
            "minimum of confidence of confidence after preprocessing",
            "maximum of confidence before preprocessing",
            "maximum of confidence of confidence after preprocessing",
            "maximum of difference in confidence",
            "maximum of percentage difference in confidence",
            "sum of confidence before preprocessing",
            "sum of confidence after preprocessing",
            "standard deviation of confidence before preprocessing",
            "standard deviation of confidence after preprocessing",
            "standard deviation of difference in confidence",
            "standard deviation of percentage difference in confidence",
            "number of confidences under 25 before preprocessing",
            "number of confidences under 25 after preprocessing",
            "number of confidences under 50 before preprocessing",
            "number of confidences under 50 after preprocessing",
        ]
    )

    # Get unique page numbers from the evaluation DataFrame
    page_numbers = list(evaluation_of_comparison_DataFrame["Page"].unique())
    page_numbers.append("Whole Document")

    # Iterate over each page number
    for page in page_numbers:
        if page != "Whole Document":
            # Filter the ocrdata_comparison_before_after_preprocessing DataFrame for the current page
            ocrdata_per_page = ocrdata_comparison_before_after_preprocessing[ocrdata_comparison_before_after_preprocessing["Page"] == page]
        else:
            # Use the entire ocrdata_comparison_before_after_preprocessing DataFrame for the "Whole Document" page
            ocrdata_per_page = ocrdata_comparison_before_after_preprocessing

        # Calculate statistic values per page using utility functions
        number_of_compared_words = utils.get_number_of_compared_words(ocrdata_per_page)
        average_confidence_before_preprocessing = utils.get_average_confidence_before_preprocessing(ocrdata_per_page)
        average_confidence_after_preprocessing = utils.get_average_confidence_after_preprocessing(ocrdata_per_page)
        average_difference_in_confidence = utils.get_average_difference_in_confidence(ocrdata_per_page)
        average_percentage_difference_in_confidence = utils.get_average_percentage_difference_in_confidence(ocrdata_per_page)
        minimum_of_confidence_before_preprocessing = utils.get_minimum_of_confidence_before_preprocessing(ocrdata_per_page)
        minimum_of_confidence_of_confidence_after_preprocessing = utils.get_minimum_of_confidence_after_preprocessing(ocrdata_per_page)
        maximum_of_confidence_before_preprocessing = utils.get_maximum_of_confidence_before_preprocessing(ocrdata_per_page)
        maximum_of_confidence_of_confidence_after_preprocessing = utils.get_maximum_of_confidence_after_preprocessing(ocrdata_per_page)
        maximum_of_difference_in_confidence = utils.get_maximum_of_difference_in_confidence(ocrdata_per_page)
        maximum_of_percentage_difference_in_confidence = utils.get_maximum_of_percentage_difference_in_confidence(ocrdata_per_page)
        sum_of_confidence_before_preprocessing = utils.get_sum_of_confidence_before_preprocessing(ocrdata_per_page)
        sum_of_confidence_after_preprocessing = utils.get_sum_of_confidence_after_preprocessing(ocrdata_per_page)
        standard_deviation_of_confidence_before_preprocessing = utils.get_standard_deviation_of_confidence_before_preprocessing(ocrdata_per_page)
        standard_deviation_of_confidence_after_preprocessing = utils.get_standard_deviation_of_confidence_after_preprocessing(ocrdata_per_page)
        standard_deviation_of_difference_in_confidence = utils.get_standard_deviation_of_difference_in_confidence(ocrdata_per_page)
        standard_deviation_of_percentage_difference_in_confidence = utils.get_standard_deviation_of_percentage_difference_in_confidence(ocrdata_per_page)
        number_of_confidences_under_25_before_preprocessing = utils.get_number_of_confidences_under_25_before_preprocessing(ocrdata_per_page)
        number_of_confidences_under_25_after_preprocessing = utils.get_number_of_confidences_under_25_after_preprocessing(ocrdata_per_page)
        number_of_confidences_under_50_before_preprocessing = utils.get_number_of_confidences_under_50_before_preprocessing(ocrdata_per_page)
        number_of_confidences_under_50_after_preprocessing = utils.get_number_of_confidences_under_50_after_preprocessing(ocrdata_per_page)
 
        # Create a new row with the calculated values
        new_row = {
            "Page": page,
            "Number of compared words": number_of_compared_words,
            "average confidence before preprocessing": average_confidence_before_preprocessing,
            "average confidence after preprocessing": average_confidence_after_preprocessing,
            "average difference in confidence": average_difference_in_confidence,
            "average percentage difference in confidence": average_percentage_difference_in_confidence,
            "minimum of confidence before preprocessing": minimum_of_confidence_before_preprocessing,
            "minimum of confidence of confidence after preprocessing": minimum_of_confidence_of_confidence_after_preprocessing,
            "maximum of confidence before preprocessing": maximum_of_confidence_before_preprocessing,
            "maximum of confidence of confidence after preprocessing": maximum_of_confidence_of_confidence_after_preprocessing,
            "maximum of difference in confidence": maximum_of_difference_in_confidence,
            "maximum of percentage difference in confidence": maximum_of_percentage_difference_in_confidence,
            "sum of confidence before preprocessing": sum_of_confidence_before_preprocessing,
            "sum of confidence after preprocessing": sum_of_confidence_after_preprocessing,
            "standard deviation of confidence before preprocessing": standard_deviation_of_confidence_before_preprocessing,
            "standard deviation of confidence after preprocessing": standard_deviation_of_confidence_after_preprocessing,
            "standard deviation of difference in confidence": standard_deviation_of_difference_in_confidence,
            "standard deviation of percentage difference in confidence": standard_deviation_of_percentage_difference_in_confidence,
            "number of confidences under 25 before preprocessing": number_of_confidences_under_25_before_preprocessing,
            "number of confidences under 25 after preprocessing": number_of_confidences_under_25_after_preprocessing,
            "number of confidences under 50 before preprocessing": number_of_confidences_under_50_before_preprocessing,
            "number of confidences under 50 after preprocessing": number_of_confidences_under_50_after_preprocessing,
        }

        # Append the new row to the evaluation_of_comparison_DataFrame
        new_row = pd.DataFrame(new_row, index=[page])
        evaluation_of_comparison_DataFrame = pd.concat([evaluation_of_comparison_DataFrame, new_row], axis=0, ignore_index=True)

    # Return the evaluation_of_comparison_DataFrame
    return evaluation_of_comparison_DataFrame

def plot_confidences_before_after_preprocessing(ocrdata_without_preprocessing: pd.DataFrame, ocrdata_with_preprocessing: pd.DataFrame):
    """ Plot the confidences before and after preprocessing"""
    
    # Create a new figure and a single axes object
    fig, axes = plt.subplots()  
    # Get the confidences from the ocrdata_without_preprocessing DataFrame and plot the histogram
    ocrdata_without_preprocessing["conf"].hist(ax=axes, bins=20, alpha=0.5, label='Before Preprocessing')
    # Get the confidences from the ocrdata_with_preprocessing DataFrame and plot the histogram in green
    ocrdata_with_preprocessing["conf"].hist(ax=axes, bins=20, alpha=0.5, color="green", label='After Preprocessing')

    # Set the label for the X-axis
    axes.set_xlabel('Confidence')
    # Set the label for the Y-axis
    axes.set_ylabel('Frequency') 
    # Set the X-axis limits
    axes.set_xlim(0, 100)  
    # Display the legend in the upper left corner
    axes.legend(loc="upper left")  
    
    # Set the x-axis tick marks so that labels for values from 0 to 100 with a step size of 5 are created
    x_ticks = [i for i in range(0, 101, 5)]  
    axes.set_xticks(x_ticks)

    # Save the figure as an image file in the specified output folder
    fig.savefig('outputfolder/ocrdata_hist.png')  # Save the figure as an image file in the specified output folder






