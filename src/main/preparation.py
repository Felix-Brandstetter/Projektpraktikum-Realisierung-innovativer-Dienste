from wand.image import Image
import wand
import os
import shutil
import fitz


def get_file_format(file):
    try:
        with Image(filename=file) as image:
            return image.format
    except wand.exceptions.CorruptImageError:
        # TODO Was passiert mit Bildern die nicht eingelesen werden können
        print("Bild konnte nicht eingelesen werden")
        move_file_to_folder(file, "/RIDSS2023/outputfolder/failed", override=True)
    except wand.exceptions.BlobError:
        print("File not found")
    except Exception as e:
        print(e)
        print("Anderes Problem")


def move_file_to_folder(file, destination_folder, override=True):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    destination_filepath = os.path.join(destination_folder, os.path.basename(file))
    if override:
        shutil.move(file, destination_filepath)
    else:
        if not os.path.exists(destination_filepath):
            shutil.move(file, destination_filepath)


def is_pdf_digital(file):
    pdf_is_digital = True
    with fitz.open(file) as pdf:
        for page in pdf:
            page_text = page.get_text()
            if len(page_text) < 180:
                print("Pdf is scanned")
                pdf_is_digital = False
                break
    return pdf_is_digital


def get_metadata(file):
    metadata = {}
    with Image(filename=file) as image:
        metadata.update((k, v) for k, v in image.metadata.items())
    print(metadata)


def convert_to_pdf(file):
    with Image(filename=file, resolution=300) as image:
        image.format = 'pdf'
        filename=os.path.join('/RIDSS2023/tmp', os.path.splitext(os.path.basename(file))[0]+'.pdf')
        print(filename)
        image.save(filename=filename)
    return filename
        