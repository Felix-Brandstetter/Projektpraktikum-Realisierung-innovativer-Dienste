import os
import fitz
from wand.image import Image
import pytesseract
from pytesseract import Output
from fitz import Page
import glob
import re
import sys
import pandas



def main(file):
    #Convert PDF to JPEG
    path_to_converted_jpegs = os.path.join("/RIDSS2023/tmp",os.path.splitext(os.path.basename(file))[0])
    os.makedirs(path_to_converted_jpegs, exist_ok=True)
    convert_pdf_to_multiple_jpeg(file_path=file,destination_folder=path_to_converted_jpegs)
    jpegs = glob.glob(path_to_converted_jpegs + "/*.jpg")
    
    
    #Open PDF
    with fitz.open(file) as pdf:
        for page_no, page in enumerate(pdf):
            width = min(page.rect[2], page.rect[3])
            scale = 2500.0 / width
            jpeg = jpegs[page_no]
            ocr_data = ocr_data = pytesseract.image_to_data(
                jpeg,
                lang="deu",
                config="",
                nice=0,
                output_type=Output.STRING,
                timeout=0,
                pandas_config=None,
            )
            print(ocr_data)
            for num, box in enumerate(ocr_data.splitlines()):
                if num != 0:
                    box = box.split()
                    if len(box) == 12:
                        left = int(box[6])
                        right = int(box[6]) + int(box[8])
                        top = int(box[7])
                        bottom = int(box[7]) + int(box[9])
                        text = box[11]
                        word = (left, top, right, bottom, text, scale)
                        page = write_word_in_pdf_page(page, word)

        pdf.save(file.replace(".pdf", ".ocr.pdf"))



def write_word_in_pdf_page(pdf_page:Page,word):
    rect = fitz.Rect(word[0], word[1], word[2], word[3])
    pdf_page.draw_rect(rect, color=(1, 0, 0))
    text = word[4]
    letters_top_0 = "ÄÖÜ"
    letters_top_1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZbdfhikltj0123456789/\\§$%&?(){}[]"

    letters_size_0 = "j(){}[]§"
    letters_size_1 = "ÄÖÜ"
    letters_size_2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZbdfhiklt0123456789/\\$%&?"
    letters_size_3 = "gpqy"

    font_size_pixel = 2

    if bool(re.match(r'\w*[' + letters_top_0 + r']\w*', text)):
        translation = 0.2
    elif bool(re.match(r'\w*[' + letters_top_1 + r']\w*', text)):
        translation = 0.45
    else:
        translation = 0.55

    if bool(re.match(r'\w*[' + letters_size_1 + r']\w*', text)) and (
            bool(re.match(r'\w*[' + letters_size_0 + r']\w*', text)) or bool(
            re.match(r'\w*[' + letters_size_3 + r']\w*', text))):
        scale = 0.9
    elif bool(re.match(r'\w*[' + letters_size_2 + r']\w*', text)) and (
            bool(re.match(r'\w*[' + letters_size_0 + r']\w*', text)) or bool(
            re.match(r'\w*[' + letters_size_3 + r']\w*', text))):
        scale = 1.0
    elif bool(re.match(r'\w*[' + letters_size_3 + r']\w*', text)):
        scale = 1.4

    elif bool(re.match(r'\w*[' + letters_size_0 + r']\w*', text)):
        scale = 1.1
    elif bool(re.match(r'\w*[' + letters_size_1 + r']\w*', text)):
        scale = 1.2
    elif bool(re.match(r'\w*[' + letters_size_2 + r']\w*', text)):
        scale = 1.40
    else:
        scale = 1.94


    scale_x = (rect.x1 - rect.x0) / fitz.get_text_length(text, fontsize=2)

    pdf_page.insert_textbox(rect, text, fontsize=2, color=(1, 0, 0), fontname='helv',
                            morph=(fitz.Point(rect.x0, rect.y0 + font_size_pixel * translation),
                                   fitz.Matrix(scale_x, scale * (rect.y1 - rect.y0) / font_size_pixel)))

    return pdf_page


def convert_pdf_to_multiple_jpeg(file_path: str, destination_folder: str):
    with Image(filename=file_path) as image:
        image.format = "jpg"
        image.compression_quality = 100
        image.resolution = 300
        image.resize(210,297)
        filename = os.path.join(
            destination_folder, os.path.splitext(os.path.basename(file_path))[0] + ".jpg"
        )
        image.save(filename=filename)
    return filename

if __name__ == "__main__":
    main("/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf")
