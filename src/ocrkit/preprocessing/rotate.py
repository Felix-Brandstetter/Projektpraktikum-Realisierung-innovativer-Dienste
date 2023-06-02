import pytesseract
from wand.image import Image
import os
import ocrkit.preprocessing.utils as utils


def convert_to_tiff(pdf, output_folder):
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    outfile = os.path.join(output_folder, os.path.basename(pdf) + ".tiff")
    with Image(filename=pdf, resolution=300) as img:
        img.format = "tiff"
        img.depth = 8
        img.alpha_channel = "off"
        img.save(filename=outfile)
    return outfile


input_pdf = "/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-04.pdf"
a = convert_to_tiff(input_pdf, "tmp")

orientation = pytesseract.image_to_osd(a)
print (orientation)

