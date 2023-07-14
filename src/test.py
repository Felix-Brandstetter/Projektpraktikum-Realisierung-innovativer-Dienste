import ocrmypdf
from pathlib import Path

input_file = "Testdateien/ToOcr-07.pdf"
output_file = "output/OCRTestDocument.pdf"

#ocrmypdf.configure_logging(2)

ocrmypdf.ocr(
    input_file=Path(input_file),
    output_file=Path(output_file),
    image_dpi=150,
    force_ocr=True,
    rotate_pages=True,
    rotate_pages_threshold = 14.0,
    pdf_renderer="hocr",
    
    
    #Ridss2023 Options
    binarization_method=1,
    normalize_contrast=True,
    improve_contrast=False,
    sharpen_edges=False,
    deskew_opencv=False,
    rotate_image_to_correct_text_orientation=False,
    font_color_pdf="red",
    #visible_text=True
    
)
