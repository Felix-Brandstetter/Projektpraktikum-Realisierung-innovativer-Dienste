import ocrkit

# Create new Inputfile
inputpdf = ocrkit.InputPDF("/RIDSS2023/src/tests/test_ressources/test_rotate/test_image.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()
list_pages  = tiff_image.split_tiff_image()

a = ocrkit.get_rotation_angel(tiff_image)
print(a)
for page in list_pages:
    a = ocrkit.get_rotation_angel(page)
    print(a)