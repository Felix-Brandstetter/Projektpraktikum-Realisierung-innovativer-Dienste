import sys
from datetime import datetime


sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrkit
import sys
import utils

# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/ToOcr-30.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff_with_ghostscript()
tiff_image.save_image("Test.tiff")


# Get OCRDATA and record the runtime of OCR
startTime_eng = datetime.now()
ocrdata_englisch = ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="eng"
)
runtime_eng = datetime.now() - startTime_eng

startTime_deu = datetime.now()
ocrdata_deutsch = ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="deu"
)
runtime_deu = datetime.now() - startTime_deu

startTime_chi_sim = datetime.now()
ocrdata_chi_sim = ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="chi_sim"
)
runtime_chi_sim = datetime.now() - startTime_chi_sim

startTime_eng_deu_chi_sim = datetime.now()
ocrdata_eng_deu_chi_sim = ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="deu+eng+chi_sim"
)
runtime_eng_deu_chi_sim = datetime.now() - startTime_eng_deu_chi_sim

startTime_all_languages = datetime.now()
ocrdata_all_languages= ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="ita+ara+fin+dan+fra+hin+spa+por+deu+eng+chi_sim+"
)
runtime_all_languages = datetime.now() - startTime_all_languages

startTime_eng_chi_sim = datetime.now()
ocrdatachi_eng_chi_sim= ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="eng+chi_sim"
)
runtime_eng_chi_sim = datetime.now() - startTime_eng_chi_sim

startTime_eng_deu = datetime.now()
ocrdata_eng_deu = ocrkit.get_ocr_data(
    delete_minus1_confidences=False,
    tiff_image=tiff_image, language="eng+deu"
)
runtime_eng_deu = datetime.now() - startTime_eng_deu

#Get the average confidence and the sum of confidence for the different languages
evaluation_ocrdata_englisch = utils.evaluate_ocrdata(ocrdata_englisch)
row1_englisch = evaluation_ocrdata_englisch.iloc[0]
print("English:")
print("Sum: " + str(round(row1_englisch["sum_of_confidence"],0)))
print("Average: " + str(round(row1_englisch["average_confidence"],1)))
print("Runtime: " + str(round(runtime_eng.total_seconds(),1)) + "s")

evaluation_ocrdata_deutsch = utils.evaluate_ocrdata(ocrdata_deutsch)
row1_deutsch = evaluation_ocrdata_deutsch.iloc[0]
print("Deutsch:")
print("Sum: " + str(round(row1_deutsch["sum_of_confidence"],0)))
print("Average: " + str(round(row1_deutsch["average_confidence"],1)))
print("Runtime: " + str(round(runtime_deu.total_seconds(),1)) + "s")

evaluation_ocrdata_chi_sim = utils.evaluate_ocrdata(ocrdata_chi_sim)
row1_chi_sim = evaluation_ocrdata_chi_sim.iloc[0]
print("Chinese:")
print("Sum: " + str(round(row1_chi_sim["sum_of_confidence"],0)))
print("Average: " + str(round(row1_chi_sim["average_confidence"],1)))
print("Runtime: " + str(round(runtime_chi_sim.total_seconds(),1)) + "s")

evaluation_ocrdata_deu_eng_chi_sim = utils.evaluate_ocrdata(ocrdata_eng_deu_chi_sim)
row1_deu_eng_chi_sim = evaluation_ocrdata_deu_eng_chi_sim.iloc[0]
print("Deutsch, English, Chinese:")
print("Sum: " + str(round(row1_deu_eng_chi_sim["sum_of_confidence"],0)))
print("Average: " + str(round(row1_deu_eng_chi_sim["average_confidence"],1)))
print("Runtime: " + str(round(runtime_eng_deu_chi_sim.total_seconds(),1)) + "s")

evaluation_ocrdata_all_languages = utils.evaluate_ocrdata(ocrdata_all_languages)
row1_all_languages = evaluation_ocrdata_all_languages.iloc[0]
print("All Languages:")
print("Sum: " + str(round(row1_all_languages["sum_of_confidence"],0)))
print("Average: " + str(round(row1_all_languages["average_confidence"],1)))
print("Runtime: " + str(round(runtime_all_languages.total_seconds(),1)) + "s")

#evaluation_ocrdata_eng_chi_sim = utils.evaluate_ocrdata(ocrdatachi_eng_chi_sim)
#row1_eng_chi_sim = evaluation_ocrdata_eng_chi_sim.iloc[0]
#print("English, Chinese Average Confidence: " + str(row1_eng_chi_sim["average_confidence"]))
#print("English, Chinese Sum of Confidence " + str(row1_eng_chi_sim["sum_of_confidence"]))
#print("Runtime Chinese and English: " + str(runtime_eng_chi_sim))

#evaluation_ocrdata_eng_deu = utils.evaluate_ocrdata(ocrdata_eng_deu)
#row1_eng_deu = evaluation_ocrdata_eng_deu.iloc[0]
#print("English, Deutsch Average Confidence: " + str(row1_eng_deu["average_confidence"]))
#print("English, Deutsch Sum of Confidence " + str(row1_eng_deu["sum_of_confidence"]))
#print("Runtime Deutsch and English: " + str(runtime_eng_deu))

#Export the OCRdata into an Excel Document
#evaluation_ocrdata_deutsch.to_excel("evaluation_ocrdata_deutsch.xlsx")
#evaluation_ocrdata_englisch.to_excel("evaluation_ocrdata_englisch.xlsx")
#evaluation_ocrdata_chi_sim.to_excel("evaluation_ocrdata_chi_sim.xlsx")
#evaluation_ocrdata_deu_eng_chi_sim.to_excel("evaluation_ocrdata_deu_eng_chi_sim.xlsx")
#evaluation_ocrdata_all_languages.to_excel("evaluation_ocrdata_all_languages.xlsx")
#evaluation_ocrdata_eng_chi_sim.to_excel("evalution_ocrdatachi_eng_chi_sim.xlsx")
#evaluation_ocrdata_eng_deu.to_excel("evaluation_ocrdata_eng_deu.xlsx")