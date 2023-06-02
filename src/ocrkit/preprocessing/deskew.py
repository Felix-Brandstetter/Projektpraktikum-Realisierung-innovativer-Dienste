
input_pdf = "/RIDSS2023/inputfolder/ToOcr_Seiten.pdf/ToOcr-06.pdf"

from wand.image import Image
from wand.display import display


with Image(filename=input_pdf, resolution=300) as img:
    img.deskew(0.4*img.quantum_range)
    img.save(filename='form1_deskew.png')
    display(img)
