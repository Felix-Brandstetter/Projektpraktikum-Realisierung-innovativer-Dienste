import ocrmypdf
from pathlib import Path

input_file = "Testdateien/45_Grad.pdf"
output_file = "output/OCRTestDocument.pdf"

ocrmypdf.configure_logging(2)

ocrmypdf.ocr(
    input_file=Path(input_file),
    output_file=Path(output_file),
    image_dpi=150,
    force_ocr=True, # forces ocr if pdf already contains text
    rotate_pages=True, # tries to rotate pages to the correct text orientation (OSD Option of tesseract before preprocessing)
    rotate_pages_threshold = 14.0, #Confidence threshold at which pages are rotated.
    pdf_renderer="hocr", # pdf renderer. Must be "hocr" if font should be visible
    keep_temporary_files=True, 
    deskew=False,
    language="eng",
    
    
    #Ridss2023 Options
    normalize_contrast=True,
    autolevel_contrast=True,
    improve_contrast=True,
    sharpen_edges=True,
    deskew_ridss2023=True,
    rotate_image_to_correct_text_orientation=True,
    font_color_pdf="red", # fontcolor in created pdf (Pay attention to the visible text option)
    visible_text=True, #If True text is visible in created PDF
    tesseract_config= "config/tesseract-config (Sauvola).cfg", # Tesseract config to set threshold method used during binarization
    strip_existing_text = True,
    multi_angle_deskew=True,
    dewarp=True,
    remove_borders=True,
    auto_language_detection=True
    
)
