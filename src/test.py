import ocrmypdf
from pathlib import Path

ocrmypdf.ocr(
    input_file=Path("/RIDSS2023/inputfolder/OCRTestDocument.pdf"),
    output_file=Path("/RIDSS2023/outputfolder/OCRTestDocument.pdf"),
    image_dpi=300,
    force_ocr=True

)
