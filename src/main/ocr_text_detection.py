from InputFile import InputFile
import pytesseract
from pytesseract import Output

def do_ocr_text_detection(input_file: InputFile):
    #Output.DATAFRAME
    #Output.BYTES
    #Output.DICT
    #Output.STRING
    ocr_data = pytesseract.image_to_data(input_file.path_to_pdf, lang="deu", config='', nice=0, output_type=Output.STRING, timeout=0, pandas_config=None)
    print(ocr_data)