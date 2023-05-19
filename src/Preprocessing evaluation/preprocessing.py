from wand.api import library
from wand.image import Image
import os


def convert_to_tiff(pdf,output_folder):
    outfile = os.path.join(output_folder,os.path.basename(pdf) + ".tiff")
    with Image(filename=pdf, resolution=300) as img:
        img.format = "tiff"
        img.depth = 8
        img.alpha_channel = 'off'
        img.save(filename=outfile)
    return outfile

def convert_to_binary_tiff(pdf,output_folder):
    outfile = os.path.join(output_folder,os.path.basename(pdf) + "binary_image.tiff")
    with Image(filename=pdf, resolution=300) as img:
        img.format = "tiff"
        img.depth = 8
        img.mode = "grey"
        img.threshold = 0.2
        img.alpha_channel = 'off'
        img.save(filename=outfile)
    return outfile