import ocrmypdf
from pathlib import Path

input_file = "/RIDSS2023/Testdateien/ToOcr-10.pdf"
output_file = "output/WithoutPreProcessing.pdf"

ocrmypdf.configure_logging(2)


#Default ocrmypdf
ocrmypdf.ocr(
    input_file=Path(input_file),
    output_file=Path(output_file),
    image_dpi=150,
    force_ocr=True, # forces ocr if pdf already contains text
    rotate_pages=True, # tries to rotate pages to the correct text orientation (OSD Option of tesseract before preprocessing)
    rotate_pages_threshold = 4, #Confidence threshold at which pages are rotated.
    pdf_renderer="hocr", # pdf renderer. Must be "hocr" if font should be visible
    keep_temporary_files=True, 
    deskew=True,
    language="eng",
    font_color_pdf="red", # fontcolor in created pdf (Pay attention to the visible text option)
    visible_text=True, #If True text is visible in created PDF
    )


output_file = "output/WithPreprocessing.pdf"
#ocrmy pdf with preprocessing 
ocrmypdf.ocr(
    input_file=Path(input_file),
    output_file=Path(output_file),
    image_dpi=150,
    force_ocr=True, # forces ocr if pdf already contains text
    rotate_pages=True, # tries to rotate pages to the correct text orientation (OSD Option of tesseract before preprocessing)
    rotate_pages_threshold = 4, #Confidence threshold at which pages are rotated.
    pdf_renderer="hocr", # pdf renderer. Must be "hocr" if font should be visible
    keep_temporary_files=True, 
    deskew=False,
    language="eng",
    
    
    #Ridss2023 Options
    #Contrast
    normalize_contrast=False,
    autolevel_contrast=True,
    improve_contrast=False,
    sharpen_edges=False,
    adaptive_sharpen_edges=True,
    despeckle=False,
    tesseract_config= "config/tesseract-config (Otsu).cfg", # Tesseract config to set threshold method used during binarization
    
    #Text orientation
    deskew_ridss2023=True,
    rotate_image_to_correct_text_orientation=True,
    dewarp=False,
    multi_angle_deskew=False,
    
    #Borders
    remove_borders=False,
    
    #Language
    auto_language_detection=True,
    
    #Other stuff we implemented
    font_color_pdf="red", # fontcolor in created pdf (Pay attention to the visible text option)
    visible_text=True, #If True text is visible in created PDF
    strip_existing_text = True, # If True existing text is removed from pdf
)
