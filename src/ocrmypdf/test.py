from PIL import Image
import ocrmypdf


image = "/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf"
image_jpg = "/RIDSS2023/inputfolder/Testnotenauszug-01.jpg"

ocrmypdf.ocr(image_jpg,"outputfolder/pdf_with_ocr.pdf", deskew=True, image_dpi=300, skip_text=True)