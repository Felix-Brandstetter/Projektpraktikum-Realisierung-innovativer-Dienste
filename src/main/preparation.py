from wand.image import Image
import wand
import os
import shutil
import fitz
from InputFile import InputFile


def get_file_format(file_path: str):
    try:
        with Image(filename=file_path) as image:
            return image.format
    except wand.exceptions.CorruptImageError:
        # TODO Was passiert mit Bildern die nicht eingelesen werden können
        print("Bild konnte nicht eingelesen werden")
        move_file_to_folder(file_path, "/RIDSS2023/outputfolder/failed", override=True)
    except wand.exceptions.BlobError:
        print("File not found")
    except Exception as e:
        print(e)
        print("Anderes Problem")


def move_file_to_folder(file_path: str, destination_folder: str, override=True):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    destination_filepath = os.path.join(destination_folder, os.path.basename(file_path))
    if override:
        shutil.move(file_path, destination_filepath)
    else:
        if not os.path.exists(destination_filepath):
            shutil.move(file_path, destination_filepath)


def is_pdf_digital(file_path: str):
    pdf_is_digital = True
    with fitz.open(file_path) as pdf:
        for page in pdf:
            page_text = page.get_text()
            if len(page_text) < 180:
                print("Pdf is scanned")
                pdf_is_digital = False
                break
    return pdf_is_digital


def get_metadata(file_path: str):
    metadata = {}
    with Image(filename=file_path) as image:
        metadata.update((k, v) for k, v in image.metadata.items())
    print(metadata)


def convert_to_pdf(file_path: str):
    with Image(filename=file_path, resolution=300) as image:
        image.format = "pdf"
        filename = os.path.join(
            "/RIDSS2023/tmp", os.path.splitext(os.path.basename(file_path))[0] + ".pdf"
        )
        print(filename)
        image.save(filename=filename)
    return filename


def do_preperation(input_file: InputFile):
    file_format = get_file_format(input_file.path_to_original_file)
    if file_format == "PDF":
        print("Is PDF")
        input_file.path_to_pdf = input_file.path_to_original_file
        if is_pdf_digital(input_file.path_to_pdf):
            print("PDF is digital")
            move_file_to_folder(input_file, "/RIDSS2023/outputfolder", override=True)
        else:
            print("Pdf is scanned")
    else:
        print("Is no PDF")
        input_file.path_to_pdf = convert_to_pdf(input_file.path_to_original_file)
    return input_file
