from wand.image import Image
import os
import shutil


def get_file_format(file):
    with Image(filename=file) as image:
        return image.format


def copy_file_to_folder(file, destination_folder, override=True):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    destination_filepath = os.path.join(destination_folder, os.path.basename(file))
    if override:
        shutil.move(file, destination_filepath)
    else:
        if not os.path.exists(destination_filepath):
            shutil.move(file, destination_filepath)

def is_pdf_digital(pdf):
    #TODO
    print("ToDo")