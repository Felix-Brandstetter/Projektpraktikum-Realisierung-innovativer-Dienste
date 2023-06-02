from ocrkit.ocr import ocr_tools
from ocrkit import InputPDF

# Create new Inputfile
inputfile = InputPDF("/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf")


# Convert to Tiff Image
tiff_image = inputfile.convert_to_tiff()

#Preprocessing
tiff_image = tiff_image.binarize_adaptive_threshold()
tiff_image.display()



# Create Searchable PDF
ocr_tools.create_searchable_pdf(
    tiff_image=tiff_image, out_filename="outputfolder/test.pdf", language="deu"
)
