from PIL import Image
import ocrmypdf
#TODO Test optimaze Values https://ocrmypdf.readthedocs.io/en/latest/cookbook.html

image = "/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf"
image_jpg = "/RIDSS2023/inputfolder/Testnotenauszug-01.jpg"
ocrmypdf.Verbosity(2)
ocrmypdf.ocr(image_jpg,"outputfolder/pdf_with_ocr.pdf", 
             deskew=True,
             rotate_pages=True, 
             image_dpi=300,
             optimize=3,
             clean=True,
             tesseract_timeout=180,
             pdf_renderer="hocr",
             skip_text=True)