import sys

sys.path.append("/RIDSS2023/src")
sys.path.append("/RIDSS2023/src/Experimente")
from ocrkit import *
import ocrkit
import sys
import utils
import os
import shutil
from datetime import datetime
from PIL import Image

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000

# Pfad zum Eingabeordner mit den PDF-Dateien
input_folder = "/RIDSS2023/src/Experimente/Testdateien"

output_folder = "/RIDSS2023/experiment_ergebnisse/Kontrast/Binarization_Test"
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

# Liste der unterstützten Dateierweiterungen
supported_extensions = [".pdf"]

# Set MAX_IMAGE_PIXELS for Experiments
Image.MAX_IMAGE_PIXELS = 1000000000


# Iteriere über alle Dateien im Eingabeordner
for filename in os.listdir(input_folder):
    # Überprüfe, ob die Datei die unterstützte Erweiterung hat
    if any(filename.lower().endswith(ext) for ext in supported_extensions):
        # Vollständiger Pfad zur aktuellen Datei
        file_path = os.path.join(input_folder, filename)

        # Erstelle einen neuen InputPDF
        inputpdf = InputPDF(file_path)

        # Erzeuge den Ausgabepfad für die aktuellen Datei
        file_output_folder = os.path.join(output_folder, filename[:-4])

        # Lösche den Ausgabeordner, falls er bereits existiert
        if os.path.exists(file_output_folder):
            shutil.rmtree(file_output_folder)

        # Erstelle den Ausgabeordner
        os.makedirs(file_output_folder)
        tiff_image_original = inputpdf.convert_to_tiff_with_ghostscript(dpi=300)

        # Get ocrdata from Tiff Image
        ocrdata_original = ocrkit.get_ocr_data(
            tiff_image=tiff_image_original, language="deu+eng+chi_sim"
        )
        # Get Evaluation Data
        evaluation_ocrdata_original = utils.evaluate_ocrdata(ocrdata_original)

        # Save to Excel
        evaluation_ocrdata_original.to_excel(
            os.path.join(file_output_folder, f"evaluation_ocrdata_original.xlsx")
        )

        # Create Searchable PDF
        ocrkit.create_searchable_pdf(
            tiff_image=tiff_image_original,
            out_filename=os.path.join(file_output_folder, f"tiff_image_original.pdf"),
            language="deu+eng+chi_sim",
        )

        methods = [
            "kapur",
            "otsu",
            "triangle",
            "adaptive_threshold",
            "edge",
            "adaptive_threshold + edge",
            "adaptive_threshold + sharpen",
            "adaptive_threshold + adaptive_sharpen",
        ]
        for method in methods:
            # Apply Binarization
            if method == "adaptive_threshold":
                tiff_image = tiff_image_original.binarize_adaptive_threshold()
            elif method == "edge":
                tiff_image = tiff_image_original.binarize_edge(radius=1)
            elif method == "adaptive_threshold + edge":
                tiff_image = tiff_image_original.binarize_adaptive_threshold()
                tiff_image = tiff_image.binarize_edge(radius=1)
            elif method == "adaptive_threshold + sharpen":
                tiff_image = tiff_image_original.binarize_adaptive_threshold()
                tiff_image = tiff_image.sharpen()
            elif method == "adaptive_threshold + adaptive_sharpen":
                tiff_image = tiff_image_original.binarize_adaptive_threshold()
                tiff_image = tiff_image.adaptive_sharpen()
            else:
                tiff_image = tiff_image_original.binarize_auto_threshold(method=method)

            tiff_image.save_image(
                os.path.join(file_output_folder, f"tiff_image_{method}.tiff")
            )

            # Get ocrdata from Tiff Image
            ocrdata = ocrkit.get_ocr_data(
                tiff_image=tiff_image, language="deu+eng+chi_sim"
            )

            # Get Evaluation Data
            evaluation_ocrdata = utils.evaluate_ocrdata(ocrdata)

            # Save to Excel
            evaluation_ocrdata.to_excel(
                os.path.join(file_output_folder, f"evaluation_ocrdata_{method}.xlsx")
            )

            # Create Searchable PDF
            ocrkit.create_searchable_pdf(
                tiff_image=tiff_image,
                out_filename=os.path.join(
                    file_output_folder, f"tiff_image_{method}.pdf"
                ),
                language="deu+eng+chi_sim",
            )