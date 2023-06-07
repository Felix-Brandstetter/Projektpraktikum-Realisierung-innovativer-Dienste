import pandas as pd
import matplotlib.pyplot as plt


def _get_average_confidence(ocrdata: pd.DataFrame):
    average_confidence = ocrdata["conf"].mean()
    return average_confidence


def _get_number_of_detected_words(ocrdata: pd.DataFrame):
    number_of_detected_words = ocrdata["conf"].count()
    return number_of_detected_words


def _get_variance_of_confidence(ocrdata: pd.DataFrame):
    variance_of_confidence = ocrdata["conf"].var()
    return variance_of_confidence


def _get_minimum_of_confidence(ocrdata: pd.DataFrame):
    minimum_of_confidence = ocrdata["conf"].min()
    return minimum_of_confidence


def _get_maximum_of_confidence(ocrdata: pd.DataFrame):
    maximum_of_confidence = ocrdata["conf"].max()
    return maximum_of_confidence


def _get_number_of_zero_confidence(ocrdata: pd.DataFrame):
    number_of_zero_confidence = (ocrdata["conf"] == 0).sum()
    return number_of_zero_confidence


def _get_sum_of_confidence(ocrdata: pd.DataFrame):
    sum_of_confidence = (ocrdata["conf"]).sum()
    return sum_of_confidence


def _get_standard_deviation_of_confidence(ocrdata: pd.DataFrame):
    standard_deviation_of_confidence = (ocrdata["conf"]).std()
    return standard_deviation_of_confidence


def _get_number_of_confidences_under_25(ocrdata: pd.DataFrame):
    number_of_confidences_under_25 = (ocrdata["conf"] < 25).sum()
    return number_of_confidences_under_25


def _get_number_of_confidences_under_50(ocrdata: pd.DataFrame):
    number_of_confidences_under_50 = (ocrdata["conf"] < 50).sum()
    return number_of_confidences_under_50


def evaluate_ocrdata(ocrdata: pd.DataFrame):
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
        average_confidence = _get_average_confidence(ocrdata_per_page)
        number_of_detected_words = _get_number_of_detected_words(ocrdata_per_page)
        variance_of_confidence = _get_variance_of_confidence(ocrdata_per_page)
        minimum_of_confidence = _get_minimum_of_confidence(ocrdata_per_page)
        maximum_of_confidence = _get_maximum_of_confidence(ocrdata_per_page)
        number_of_zero_confidence = _get_number_of_zero_confidence(ocrdata_per_page)
        sum_of_confidence = _get_sum_of_confidence(ocrdata_per_page)
        standard_deviation_of_confidence = _get_standard_deviation_of_confidence(
            ocrdata_per_page
        )
        number_of_confidences_under_25 = _get_number_of_confidences_under_25(
            ocrdata_per_page
        )
        number_of_confidences_under_50 = _get_number_of_confidences_under_50(
            ocrdata_per_page
        )
        # Create new row
        new_row = {
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
        }

        # Append row to dataframe
        new_row = pd.DataFrame(new_row, index=[page])
        ocr_evaluation = pd.concat([ocr_evaluation, new_row], axis=0, ignore_index=True)

    print(ocr_evaluation)
    return ocr_evaluation


def plot_confidences(ocrdata: pd.DataFrame):
    fig, axes = plt.subplots()  # Erstellt eine neue Abbildung und ein einzelnes Achsenobjekt
    
    ocrdata["conf"].hist(ax=axes, bins=20)  # Das Achsenobjekt angeben, auf dem das Histogramm gezeichnet werden soll
    
    axes.set_xlabel('Confidence')  # Achsenbeschriftung für X-Achse
    axes.set_ylabel('Frequency')  # Achsenbeschriftung für Y-Achse
    axes.set_xlim(0, 100)
    
    # X-Achsenbeschriftungen festlegen
    x_ticks = [i for i in range(0, 101, 5)]  # Erzeugt Beschriftungen für Werte von 0 bis 100 mit einer Schrittweite von 10
    axes.set_xticks(x_ticks)

    fig.savefig('/RIDSS2023/ocrdata_hist.png') 
