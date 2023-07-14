import ocrmypdf
from pathlib import Path

input_file = "Testdateien/ToOcr-01.pdf"
output_file = "OCRTestDocument.pdf"

ocrmypdf.ocr(
    input_file=Path(input_file),
    output_file=Path(output_file),
    image_dpi=150,
    force_ocr=True,
    rotate_pages=True,
    rotate_pages_threshold = 14.0,
    
    #Ridss2023 Options
    binarization_method=1,
    normalize_contrast=True,
    improve_contrast=True,
    sharpen_edges=True,
    deskew_opencv=True,
    rotate_image_to_correct_text_orientation=True,
    
)
