import ocrmypdf
import os
#TODO Test optimaze Values https://ocrmypdf.readthedocs.io/en/latest/cookbook.html


def process_file_with_ocrmypdf(pdf):
    ocrmypdf.Verbosity(2)
    outfile = os.path.join("outputfolder", os.path.basename(pdf))
    print(outfile)
    ocrmypdf.ocr(pdf,
                output_file=outfile, 
                deskew=True,
                rotate_pages=True, 
                image_dpi=300,
                optimize=3,
                clean=True,
                tesseract_timeout=180,
                pdf_renderer="hocr",
                skip_text=True,
                tesseract_config="tsv")

if __name__ == "__main__":
    process_file_with_ocrmypdf("/RIDSS2023/inputfolder/Testnotenauszug_scanned.tiff")

