from PIL import Image
import pytesseract
import cv2
import wand

image = "/RIDSS2023/inputfolder/sample.pdf"

# Simple image to string
# print(pytesseract.image_to_string(Image.open(image)))


from wand.image import Image
from wand.display import display

with Image(filename=image) as img:
    print(img.size)
    for r in 1, 2, 3:
        with img.clone() as i:
            i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
            i.rotate(90 * r)
            i.save(filename="outputfolder/mona-lisa-{0}.pdf".format(r))
            display(i)