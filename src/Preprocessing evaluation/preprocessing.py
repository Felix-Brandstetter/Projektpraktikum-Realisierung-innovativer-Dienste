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
        img.transform_colorspace('gray')
        img.adaptive_threshold(width=16, height=16, offset=-0.08 * img.quantum_range)
        img.alpha_channel = 'off'
        img.save(filename=outfile)
    return outfile