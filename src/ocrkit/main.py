import os
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
import io
import os
from wand.image import Image
import glob


def process_file_with_ocrkit(file):

    #Convert PDF to Jpeg
    path_to_converted_jpegs = os.path.join("/RIDSS2023/tmp",os.path.splitext(os.path.basename(file))[0])
    os.makedirs(path_to_converted_jpegs, exist_ok=True)
    convert_pdf_to_multiple_jpeg(file_path=file,destination_folder=path_to_converted_jpegs)
    images = glob.glob(path_to_converted_jpegs + "/*.jpg")

    #Create Seracahble PDF with tesseract
    pdf_writer = PyPDF2.PdfWriter()
    for image in images:
        page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        pdf = PyPDF2.PdfReader(io.BytesIO(page))
        pdf_writer.add_page(pdf.pages[0])

    # export the searchable PDF to searchable.pdf
    with open("searchable.pdf", "wb") as f:
        pdf_writer.write(f)



def convert_pdf_to_multiple_jpeg(file_path: str, destination_folder: str):
    with Image(filename=file_path, resolution=300) as image:
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
    process_file_with_ocrkit("/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf")
