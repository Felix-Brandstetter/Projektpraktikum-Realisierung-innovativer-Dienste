from ocrkit import TiffImage
from ocrkit.ocr.hocrtransform import HocrTransform
import os
import pytesseract
from pypdf import PdfWriter
from pytesseract import Output
import re
import shutil
from datetime import datetime

## Provides functions with functionalities related to OCR. The functions allow the creation of 
## searchable PDFs, creation of hOCR files, merging of hOCR files and a one-page images, 
## obtaining the OCR results as a DataFrame and determining the rotation angle of a TiffImage



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
    """ 
    Creates a searchable PDF file from a TiffImage object.
    Splits the TiffImage into pages, generates hOCR files, and merges them with one-page images into a searchable PDF.
    The resulting PDF is saved to the specified filename. 
    """

    # Split tiff image into pages
    tiff_image_pages = tiff_image.split_tiff_image()
    # Create folder inside workfolder to store created pdf_pages
    if os.path.exists(os.path.join(tiff_image.workfolder.name, "pdf_pages")):
        shutil.rmtree(os.path.join(tiff_image.workfolder.name, "pdf_pages"))
    # Create the output folder
    os.mkdir(os.path.join(tiff_image.workfolder.name, "pdf_pages"))
    # Initialize a PdfWriter for merging pages
    merger = PdfWriter()
    
    # Loop through tiff_images/pages and create searchable PDFs
    for page_number, page in enumerate(tiff_image_pages):
        # Create hocr file
        hocr_file = _create_hocr_file_from_one_page_image(
            image=page.path, working_folder=tiff_image.workfolder, language=language
        )
        # Define the output PDF page filename
        created_pdf_page = os.path.join(
            tiff_image.workfolder.name,
            "pdf_pages",
            tiff_image.basename + "_page_{}.pdf".format(page_number),
        )
        # Merge hocr and one-page image into a searchable PDF page
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
    # Write the merged PDF file
    merger.write(out_filename)


def _create_hocr_file_from_one_page_image(image, working_folder, language):
    """ Creates a hOCR file from a single-page image using Tesseract OCR"""

    # Define the base output filename
    output_filename_base = os.path.join(working_folder.name, "hocrfile")
    # Run Tesseract OCR to generate hocr file
    ocrdata = pytesseract.pytesseract.run_tesseract(
        input_filename=image,
        output_filename_base=output_filename_base,
        lang=language,
        extension="hocr",
    )
    # Return the path to the generated hocr file
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
    """ Merges a hOCR file and a one-page image into a searchable PDF page using hocrtransform"""

    # Initialize the HocrTransform object
    hocrtransformer = HocrTransform(hocr_filename=hocr_filename, dpi=300)
    # Perform the merging of hocr and one-page image into a searchable PDF
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
    """ Performs OCR on a TiffImage and returns the OCR-Data as a DataFrame"""

    # Get the start time for measuring runtime
    start_time = datetime.now()
    # Perform OCR using pytesseract and obtain OCR data as a DataFrame
    ocrdata = pytesseract.image_to_data(
        image=tiff_image.path, output_type=Output.DATAFRAME, lang=language
    )
    # Calculate the runtime by subtracting the start time from the end time
    runtime = datetime.now() - start_time
    # Format the runtime to two decimal places
    runtime = "{:.2f}".format(runtime.total_seconds())
    # Delete OCR data rows with confidence value -1 if specified
    if delete_minus1_confidences:
        ocrdata = ocrdata[ocrdata["conf"] != -1]
    # Add the runtime column to the DataFrame
    ocrdata['runtime'] = runtime
    # Return the OCR data DataFrame
    return ocrdata

def get_rotation_angle(tiff_image: TiffImage) -> float:
    """ 
    Determines the rotation angle of a TiffImage by analyzing the 
    OSD (Orientation and Script Detection) data obtained from Tesseract OCR
    """
    
    # Initialize the angle as 0.0
    angle = 0.0
    try:
        # Perform OCR on the tiff image to obtain OSD (Orientation and Script Detection) data
        osd_data = pytesseract.image_to_osd(tiff_image.path)
        # Use regex to extract the angle value from the OSD data
        angle = re.search("(?<=Rotate: )\d+", osd_data).group(0)
        angle = float(angle)
    except pytesseract.pytesseract.TesseractError:
        # Handle the case when there are too few characters for OSD detection
        print("Too few characters. Skipping this page. Error during processing. Setting rotation angle to 0.0")
    # Return the rotation angle
    return angle
