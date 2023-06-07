import ocrkit

# Create new Inputfile
inputpdf = ocrkit.InputPDF("/RIDSS2023/inputfolder/Testnotenauszug_scanned.pdf")


# Convert to Tiff Image
tiff_image = inputpdf.convert_to_tiff()


# Preprocessing
tiff_image_preprocessed = tiff_image.binarize_adaptive_threshold()

# Save Images
tiff_image.save_image("test.tiff")
tiff_image_preprocessed.save_image("preprocessed_tiff.tiff")


# Create Searchable PDF
ocrkit.create_searchable_pdf(
    tiff_image=tiff_image,
    out_filename="outputfolder/test.pdf",
    language="deu",
    show_bounding_boxes=True,
)

# Create Searchable PDF
ocrkit.create_searchable_pdf(
    tiff_image=tiff_image_preprocessed,
    out_filename="outputfolder/test_preprocessed.pdf",
    language="deu",
    show_bounding_boxes=True,
)
