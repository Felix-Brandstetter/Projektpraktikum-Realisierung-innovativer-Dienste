import preparation
import preprocessing
import ocr_text_detection
from InputFile import InputFile


def main(file):
    input_file = InputFile(file)
    input_file = preparation.do_preperation(input_file)
    preprocessing.do_preprocessing(input_file)
    ocr_text_detection.do_ocr_text_detection(input_file)

    # preparation.move_file_to_folder(file,"/RIDSS2023/outputfolder",override=True)


if __name__ == "__main__":
    main("/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf")
