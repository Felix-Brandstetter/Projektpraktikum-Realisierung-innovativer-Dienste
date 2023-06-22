from ocrkit import TiffImage
from ocrkit.ocr.hocrtransform import HocrTransform
import os
import pytesseract
from pypdf import PdfWriter
from pytesseract import Output
import re
import shutil


def create_searchable_pdf(
    tiff_image: TiffImage,
    out_filename: str,
    language: str,
    dpi: float = 300,
    fontcolor: str = "red",
    fontname: str = "Helvetica",
    show_bounding_boxes: bool = False,
    invisible_text: bool = False,
    interword_spaces: bool = False,
):
    # Split tiff image into pages
    tiff_image_pages = tiff_image.split_tiff_image()

    # Create folder inside workfolder to store created pdf_pages

    if os.path.exists(os.path.join(tiff_image.workfolder.name, "pdf_pages")):
        shutil.rmtree(os.path.join(tiff_image.workfolder.name, "pdf_pages"))

    # Erstelle den Ausgabeordner
    os.mkdir(os.path.join(tiff_image.workfolder.name, "pdf_pages"))

    # Loop through tiff_images/pages and create searchable pdfs
    merger = PdfWriter()
    for page_number, page in enumerate(tiff_image_pages):
        # Create hocr file
        hocr_file = _create_hocr_file_from_one_page_image(
            image=page.path, working_folder=tiff_image.workfolder, language=language
        )
        created_pdf_page = os.path.join(
            tiff_image.workfolder.name,
            "pdf_pages",
            tiff_image.basename + "_page_{}.pdf".format(page_number),
        )
        # Merge tiff and hocr file
        _merge_hocr_and_one_page_image(
            hocr_filename=hocr_file,
            tiff_image=page.path,
            out_filename=created_pdf_page,
            dpi=dpi,
            fontcolor=fontcolor,
            fontname=fontname,
            show_bounding_boxes=show_bounding_boxes,
            invisible_text=invisible_text,
            interword_spaces=interword_spaces,
        )
        merger.append(created_pdf_page)

    merger.write(out_filename)


def _create_hocr_file_from_one_page_image(image, working_folder, language):
    output_filename_base = os.path.join(working_folder.name, "hocrfile")
    ocrdata = pytesseract.pytesseract.run_tesseract(
        input_filename=image,
        output_filename_base=output_filename_base,
        lang=language,
        extension="hocr",
    )

    return output_filename_base + ".hocr"


def _merge_hocr_and_one_page_image(
    hocr_filename: str,
    tiff_image: str,
    out_filename: str,
    dpi: float = 300,
    fontcolor: str = None,
    fontname: str = "Helvetica",
    show_bounding_boxes: bool = False,
    invisible_text: bool = False,
    interword_spaces: bool = False,
):
    hocrtransformer = HocrTransform(hocr_filename=hocr_filename, dpi=300)
    hocrtransformer._to_pdf(
        out_filename=out_filename,
        tiff_image=tiff_image,
        fontcolor=fontcolor,
        fontname=fontname,
        show_bounding_boxes=show_bounding_boxes,
        invisible_text=invisible_text,
        interword_spaces=interword_spaces,
    )


def get_ocr_data(
    tiff_image: TiffImage, language: str, delete_minus1_confidences: bool = True
):
    ocrdata = pytesseract.image_to_data(
        image=tiff_image.path, output_type=Output.DATAFRAME, lang=language
    )
    if delete_minus1_confidences:
        ocrdata = ocrdata[ocrdata["conf"] != -1]
    return ocrdata


def get_rotation_angle(tiff_image: TiffImage) -> float:
    angle = 0.0
    try:
        osd_data = pytesseract.image_to_osd(tiff_image.path)
        # using regex we search for the angle(in string format) of the text
        angle = re.search("(?<=Rotate: )\d+", osd_data).group(0)
        angle = float(angle)
    except pytesseract.pytesseract.TesseractError:
        print(
            "Too few characters. Skipping this page Error during processing. Setting rotationangle to 0.0"
        )
    return angle
