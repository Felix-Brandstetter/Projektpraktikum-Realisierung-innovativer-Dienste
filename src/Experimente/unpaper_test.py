import sys

sys.path.append("/RIDSS2023/src")
from ocrkit import *
import ocrmypdf
from pathlib import Path


# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/OCRTestDocument.pdf")
ocrmypdf.ocr(
    input_file=Path(inputpdf.path),
    output_file=Path("Preprocessed.pdf"),
    rotate_pages=True,
    #remove_background=True,
    deskew=True,
    clean=True,
    clean_final=True,
    tesseract_timeout=0,
    force_ocr=True
)
