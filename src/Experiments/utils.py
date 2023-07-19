import pandas as pd
import matplotlib.pyplot as plt

## Provides functions to evaluate OCR-Data created in the Experiments

def _get_average_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the average confidence of the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The average confidence.
    """
    average_confidence = ocrdata["conf"].mean()
    return average_confidence

def get_average_confidence_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the average confidence before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The average confidence before preprocessing.
    """
    average_confidence_before_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_before"].mean()
    return average_confidence_before_preprocessing

def get_average_confidence_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the average confidence after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The average confidence after preprocessing.
    """
    average_confidence_after_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_after"].mean()
    return average_confidence_after_preprocessing

def get_average_difference_in_confidence(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the average difference in confidence of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The average difference in confidence.
    """
    average_difference_in_confidence = ocrdata_comparison_before_after_preprocessing["difference_in_confidence"].mean()
    return average_difference_in_confidence

def get_average_percentage_difference_in_confidence(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the average percentage difference in confidence of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The average percentage difference in confidence.
    """
    average_percentage_difference_in_confidence = ocrdata_comparison_before_after_preprocessing["percentage_difference_confidence"].mean()
    return average_percentage_difference_in_confidence

def _get_number_of_detected_words(ocrdata: pd.DataFrame):
    """
    Calculates the number of detected words in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        int: The number of detected words.
    """
    number_of_detected_words = ocrdata["conf"].count()
    return number_of_detected_words

def get_number_of_compared_words(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the number of words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        int: The number of compared words.
    """
    number_of_compared_words = ocrdata_comparison_before_after_preprocessing["confidence_before"].count()
    return number_of_compared_words

def _get_variance_of_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the variance of the confidences in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The variance of the confidences.
    """
    variance_of_confidence = ocrdata["conf"].var()
    return variance_of_confidence

def _get_minimum_of_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the minimum confidence in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The minimum confidence.
    """
    minimum_of_confidence = ocrdata["conf"].min()
    return minimum_of_confidence

def get_minimum_of_confidence_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the minimum confidence before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The minimum confidence before preprocessing.
    """
    minimum_of_confidence_before_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_before"].min()
    return minimum_of_confidence_before_preprocessing

def get_minimum_of_confidence_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the minimum confidence after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The minimum confidence after preprocessing.
    """
    minimum_of_confidence_after_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_after"].min()
    return minimum_of_confidence_after_preprocessing

def _get_maximum_of_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the maximum confidence in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The maximum confidence.
    """
    maximum_of_confidence = ocrdata["conf"].max()
    return maximum_of_confidence

def get_maximum_of_confidence_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the maximum confidence before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The maximum confidence before preprocessing.
    """
    maximum_of_confidence_before_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_before"].max()
    return maximum_of_confidence_before_preprocessing

def get_maximum_of_confidence_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the maximum confidence after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The maximum confidence after preprocessing.
    """
    maximum_of_confidence_after_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_after"].max()
    return maximum_of_confidence_after_preprocessing

def get_maximum_of_difference_in_confidence(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the biggest difference in confidence of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The biggest difference in confidence.
    """
    maximum_of_difference_in_confidence = ocrdata_comparison_before_after_preprocessing["difference_in_confidence"].mean()
    return maximum_of_difference_in_confidence

def get_maximum_of_percentage_difference_in_confidence(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the biggest percentage difference in confidence of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The biggest percentage difference in confidence.
    """
    maximum_of_percentage_difference_in_confidence = ocrdata_comparison_before_after_preprocessing["percentage_difference_confidence"].mean()
    return maximum_of_percentage_difference_in_confidence

def _get_number_of_zero_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the number of confidences with the value 0 in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        int: The number of confidences with the value 0.
    """
    number_of_zero_confidence = (ocrdata["conf"] == 0).sum()
    return number_of_zero_confidence

def _get_sum_of_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the sum of the confidences in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The sum of the confidences.
    """
    sum_of_confidence = (ocrdata["conf"]).sum()
    return sum_of_confidence

def get_sum_of_confidence_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the sum of confidences before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The sum of confidences before preprocessing.
    """
    sum_of_confidence_before_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_before"].sum()
    return sum_of_confidence_before_preprocessing

def get_sum_of_confidence_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the sum of confidences after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The sum of confidences after preprocessing.
    """
    sum_of_confidence_after_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_after"].sum()
    return sum_of_confidence_after_preprocessing

def _get_standard_deviation_of_confidence(ocrdata: pd.DataFrame):
    """
    Calculates the standard deviation of the confidences in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The standard deviation of the confidences.
    """
    standard_deviation_of_confidence = (ocrdata["conf"]).std()
    return standard_deviation_of_confidence

def get_standard_deviation_of_confidence_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the standard deviation of confidences before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The standard deviation of confidences before preprocessing.
    """
    standard_deviation_of_confidence_before_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_before"].std()
    return standard_deviation_of_confidence_before_preprocessing

def get_standard_deviation_of_confidence_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the standard deviation of confidences after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The standard deviation of confidences after preprocessing.
    """
    standard_deviation_of_confidence_after_preprocessing = ocrdata_comparison_before_after_preprocessing["confidence_after"].std()
    return standard_deviation_of_confidence_after_preprocessing

def get_standard_deviation_of_difference_in_confidence(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the standard deviation of the differences in confidences of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The standard deviation of the differences in confidences.
    """
    standard_deviation_of_difference_in_confidence = ocrdata_comparison_before_after_preprocessing["difference_in_confidence"].std()
    return standard_deviation_of_difference_in_confidence

def get_standard_deviation_of_percentage_difference_in_confidence(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the standard deviation of the percentage differences in confidences of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        float: The standard deviation of the percentage differences in confidences.
    """
    standard_deviation_of_difference_in_confidence = ocrdata_comparison_before_after_preprocessing["percentage_difference_confidence"].std()
    return standard_deviation_of_difference_in_confidence

def _get_number_of_confidences_under_25(ocrdata: pd.DataFrame):
    """
    Calculates the number of confidences under 25 in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        int: The number of confidences under 25.
    """
    number_of_confidences_under_25 = (ocrdata["conf"] < 25).sum()
    return number_of_confidences_under_25

def get_number_of_confidences_under_25_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the number of confidences under 25 before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        int: The number of confidences under 25 before preprocessing.
    """
    number_of_confidences_under_25_before_preprocessing = (ocrdata_comparison_before_after_preprocessing["confidence_before"] < 25).sum()
    return number_of_confidences_under_25_before_preprocessing

def get_number_of_confidences_under_25_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the number of confidences under 25 after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        int: The number of confidences under 25 after preprocessing.
    """
    number_of_confidences_under_25_after_preprocessing = (ocrdata_comparison_before_after_preprocessing["confidence_after"] < 25).sum()
    return number_of_confidences_under_25_after_preprocessing

def _get_number_of_confidences_under_50(ocrdata: pd.DataFrame):
    """
    Calculates the number of confidences under 50 in the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        int: The number of confidences under 50.
    """
    number_of_confidences_under_50 = (ocrdata["conf"] < 50).sum()
    return number_of_confidences_under_50

def get_number_of_confidences_under_50_before_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the number of confidences under 50 before preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        int: The number of confidences under 50 before preprocessing.
    """
    number_of_confidences_under_50_before_preprocessing = (ocrdata_comparison_before_after_preprocessing["confidence_before"] < 50).sum()
    return number_of_confidences_under_50_before_preprocessing

def get_number_of_confidences_under_50_after_preprocessing(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Calculates the number of confidences under 50 after preprocessing of the words in the before/after preprocessing comparison.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.

    Returns:
        int: The number of confidences under 50 after preprocessing.
    """
    number_of_confidences_under_50_after_preprocessing = (ocrdata_comparison_before_after_preprocessing["confidence_after"] < 50).sum()
    return number_of_confidences_under_50_after_preprocessing

def _get_runtime(ocrdata: pd.DataFrame):
    """
    Retrieves the OCR runtime from the OCR data.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        float: The OCR runtime.
    """
    runtime = ocrdata["runtime"].values[0]
    return runtime

def evaluate_ocrdata(ocrdata: pd.DataFrame):
    """
    Evaluates the OCR data and calculates various statistics.

    Parameters:
        ocrdata (pd.DataFrame): DataFrame containing the OCR data.

    Returns:
        pd.DataFrame: DataFrame containing the evaluation results.
    """
    # Create an empty DataFrame to store the evaluation results and 
    # set the column titles for all the statistics to be included in the evaluation
    ocr_evaluation = pd.DataFrame(
        columns=[
            "Page",
            "average_confidence",
            "number_of_detected_words",
            "variance_of_confidence",
            "standard_deviation_of_confidence",
            "sum_of_confidence",
            "minimum_of_confidence",
            "maximum_of_confidence",
            "number_of_zero_confidence",
            "number_of_confidences_under_25",
            "number_of_confidences_under_50",
            "runtime",
        ]
    )

    # Get the unique page numbers from the OCR data
    unique_pages = ocrdata["page_num"].unique()

    # Iterate over each page and calculate the statistics
    for page in unique_pages:
        # Filter the OCR data for the current page
        page_data = ocrdata[ocrdata["page_num"] == page]

        # Calculate the statistics for the current page
        average_confidence = _get_average_confidence(page_data)
        number_of_detected_words = _get_number_of_detected_words(page_data)
        variance_of_confidence = _get_variance_of_confidence(page_data)
        standard_deviation_of_confidence = _get_standard_deviation_of_confidence(page_data)
        sum_of_confidence = _get_sum_of_confidence(page_data)
        minimum_of_confidence = _get_minimum_of_confidence(page_data)
        maximum_of_confidence = _get_maximum_of_confidence(page_data)
        number_of_zero_confidence = _get_number_of_zero_confidence(page_data)
        number_of_confidences_under_25 = _get_number_of_confidences_under_25(page_data)
        number_of_confidences_under_50 = _get_number_of_confidences_under_50(page_data)
        runtime = _get_runtime(page_data)

        # Create a dictionary to store the evaluation results for the current page
        evaluation_results = {
            "Page": page,
            "average_confidence": average_confidence,
            "number_of_detected_words": number_of_detected_words,
            "variance_of_confidence": variance_of_confidence,
            "standard_deviation_of_confidence": standard_deviation_of_confidence,
            "sum_of_confidence": sum_of_confidence,
            "minimum_of_confidence": minimum_of_confidence,
            "maximum_of_confidence": maximum_of_confidence,
            "number_of_zero_confidence": number_of_zero_confidence,
            "number_of_confidences_under_25": number_of_confidences_under_25,
            "number_of_confidences_under_50": number_of_confidences_under_50,
            "runtime": runtime,
        }

        # Append the evaluation results for the current page to the main evaluation DataFrame
        new_row = pd.DataFrame(evaluation_results, index=[page])
        ocr_evaluation = pd.concat([ocr_evaluation, new_row], axis=0, ignore_index=True)

    return ocr_evaluation

def plot_confidence_comparison(ocrdata_comparison_before_after_preprocessing: pd.DataFrame):
    """
    Plots a comparison of OCR confidences before and after preprocessing.

    Parameters:
        ocrdata_comparison_before_after_preprocessing (pd.DataFrame): DataFrame containing the comparison data.
    """
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Generate the x-axis values for the plot (word indices)
    x = ocrdata_comparison_before_after_preprocessing.index

    # Plot the confidence values before preprocessing as a blue line
    ax.plot(x, ocrdata_comparison_before_after_preprocessing["confidence_before"], color="blue", label="Before Preprocessing")

    # Plot the confidence values after preprocessing as a red line
    ax.plot(x, ocrdata_comparison_before_after_preprocessing["confidence_after"], color="red", label="After Preprocessing")

    # Add labels and a legend to the plot
    ax.set_xlabel("Word Index")
    ax.set_ylabel("Confidence")
    ax.legend()

    # Show the plot
    plt.show()
