import ocrkit

# Create new Inputfile
inputpdf = ocrkit.InputPDF("src/tests/test_ressources/test_deskew/test_image.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()


#Preprocessing
tiff_image_preprocessed = tiff_image.deskew()

#Save Images
tiff_image.save_image("test.tiff")
tiff_image_preprocessed.save_image("preprocessed_tiff.tiff")


# Create Searchable PDF
ocrkit.create_searchable_pdf(
    tiff_image=tiff_image, out_filename="outputfolder/test.pdf", language="deu"
)
