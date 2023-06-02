from ocrkit import TiffImage
from wand.image import Image
from ocrkit.ocr.hocrtransform import HocrTransform
import os
import glob
import pytesseract
from PyPDF2 import PdfMerger


def create_searchable_pdf(tiff_image: TiffImage, out_filename: str, language: str):
    # Split preprocessed_tiff_image in seperated pages
    #TODO in Funktion
    with Image(filename=tiff_image.path) as img:
        img.save(
            filename=os.path.join(
                tiff_image.workfolder.name, tiff_image.basename + "-page_%00000d.tif"
            )
        )
    pages = glob.glob(
        os.path.join(tiff_image.workfolder.name, tiff_image.basename + "-page_*.tif")
    )

    # Create folder inside workfolder to store created pdf_pages
    os.mkdir(os.path.join(tiff_image.workfolder.name, "pdf_pages"))

    # Loop through tiff_images/pages and create searchable pdfs
    merger = PdfMerger()
    for page_number, page in enumerate(pages):
        # Create hocr file
        hocr_file = _create_hocr_file_from_one_page_image(
            image=page, working_folder=tiff_image.workfolder, language=language
        )
        created_pdf_page = os.path.join(
            tiff_image.workfolder.name,
            "pdf_pages",
            tiff_image.basename + "_page_{}.pdf".format(page_number),
        )
        # Merge tiff and hocr file
        _merge_hocr_and_one_page_image(
            hocr_filename=hocr_file,
            tiff_image=page,
            out_filename=created_pdf_page,
            dpi=300,
            fontcolor="red",
            fontname="Helvetica",
            show_bounding_boxes=False,
            invisible_text=False,
            interword_spaces=False,
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
