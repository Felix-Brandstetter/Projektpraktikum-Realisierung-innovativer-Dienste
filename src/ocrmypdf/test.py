from PIL import Image
import ocrmypdf


image = "/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf"

ocrmypdf.ocr(image,"test.pdf", deskew=True, image_dpi=300)