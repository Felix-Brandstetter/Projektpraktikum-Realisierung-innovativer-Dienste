import ocrmypdf
from pathlib import Path

input_file = "Testdateien/ToOcr-01.pdf"
output_file = "output/OCRTestDocument1.pdf"

ocrmypdf.configure_logging(2)

ocrmypdf.ocr(
    input_file=Path(input_file),
    output_file=Path(output_file),
    image_dpi=150,
    force_ocr=True,
    rotate_pages=True,
    rotate_pages_threshold = 14.0,
    pdf_renderer="hocr",
    keep_temporary_files=True,
    
    
    #Ridss2023 Options
    normalize_contrast=True,
    improve_contrast=False,
    sharpen_edges=False,
    deskew_opencv=False,
    rotate_image_to_correct_text_orientation=False,
    font_color_pdf="red",
    visible_text=True,
    tesseract_config= "tesseract-config (Otsu).cfg"
    
)
