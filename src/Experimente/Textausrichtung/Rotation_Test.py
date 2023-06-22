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

# Setze die maximale Anzahl von Pixeln für Bilder fest
Image.MAX_IMAGE_PIXELS = 1000000000

# Festlege des Ausgabeordners für die Ergebnisse
output_folder = "/RIDSS2023/experiment_ergebnisse/Textausrichtung/Rotation_Test"

# Überprüfe, ob der Ausgabeordner bereits existiert, und lösche ihn gegebenenfalls
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

# Erstelle den Ausgabeordner
os.makedirs(output_folder)

# Pfad zum Eingabeordner mit den richtig rotierten PDF-Dateien
pdfs_with_correct_rotation = os.listdir(
    "/RIDSS2023/src/Experimente/Textausrichtung/Richtig_Rotierte_PDFs"
)

# Pfad zum Eingabeordner mit den falsch rotierten PDF-Dateien
pdfs_with_wrong_rotation = os.listdir(
    "/RIDSS2023/src/Experimente/Textausrichtung/Falsch_Rotierte_PDFs"
)


print(len(pdfs_with_correct_rotation))
print(len(pdfs_with_wrong_rotation))
# Überprüfe, ob die Anzahl der Dateien in beiden Ordnern gleich ist
if len(pdfs_with_correct_rotation) == len(pdfs_with_wrong_rotation):
    # Durchlaufe die Dateien in beiden Ordnern gleichzeitig
    for pdf_correct_rotated, pdf_wrong_rotated in zip(
        pdfs_with_correct_rotation, pdfs_with_wrong_rotation
    ):
        path_to_pdf_correct_rotated = os.path.join(
            "/RIDSS2023/src/Experimente/Textausrichtung/Richtig_Rotierte_PDFs",
            pdf_correct_rotated,
        )
        path_to_pdf_wrong_rotated = os.path.join(
            "/RIDSS2023/src/Experimente/Textausrichtung/Falsch_Rotierte_PDFs",
            pdf_wrong_rotated,
        )

        # Erzeuge den Ausgabepfad für die aktuelle Datei
        file_output_folder = os.path.join(
            output_folder, pdf_correct_rotated[:-4]
        )

        # Lösche den Ausgabeordner, falls er bereits existiert
        if os.path.exists(file_output_folder):
            shutil.rmtree(file_output_folder)

        # Erstelle den Ausgabeordner
        os.makedirs(file_output_folder)

        # Erstelle ein neues InputPDF-Objekt für das richtig rotierte PDF
        pdf_correct_rotated = InputPDF(path_to_pdf_correct_rotated)

        # Erstelle ein neues InputPDF-Objekt für das falsch rotierte PDF
        pdf_wrong_rotated = InputPDF(path_to_pdf_wrong_rotated)

        # Konvertiere das richtig rotierte PDF in ein TIFF-Bild mit Ghostscript
        tiff_image_correct_rotated = (
            pdf_correct_rotated.convert_to_tiff_with_ghostscript(dpi=300)
        )

        # Konvertiere das falsch rotierte PDF in ein TIFF-Bild mit Ghostscript
        tiff_image_wrong_rotated = pdf_wrong_rotated.convert_to_tiff_with_ghostscript(
            dpi=300
        )

        # Extrahiere OCR-Daten aus dem TIFF-Bild des richtig rotierten PDFs
        ocrdata_tiff_image_correct_rotated = ocrkit.get_ocr_data(
            tiff_image=tiff_image_correct_rotated, language="deu+eng+chi_sim"
        )

        # Extrahiere OCR-Daten aus dem TIFF-Bild des falsch rotierten PDFs
        ocrdata_tiff_image_wrong_rotated = ocrkit.get_ocr_data(
            tiff_image=tiff_image_wrong_rotated, language="deu+eng+chi_sim"
        )

        # Evaluieren der OCR-Daten für das richtig rotierte PDF
        evaluation_ocrdata_tiff_image_correct_rotated = utils.evaluate_ocrdata(
            ocrdata_tiff_image_correct_rotated
        )

        # Evaluieren der OCR-Daten für das falsch rotierte PDF
        evaluation_ocrdata_tiff_image_wrong_rotated = utils.evaluate_ocrdata(
            ocrdata_tiff_image_wrong_rotated
        )

        # Speichern der Evaluierungsergebnisse als Excel-Dateien
        evaluation_ocrdata_tiff_image_correct_rotated.to_excel(
            os.path.join(
                file_output_folder, "evaluation_ocrdata_correct_orientation.xlsx"
            )
        )
        evaluation_ocrdata_tiff_image_wrong_rotated.to_excel(
            os.path.join(
                file_output_folder, "evaluation_ocrdata_wrong_orientation.xlsx"
            )
        )

        # Erzeugen eines durchsuchbaren PDFs aus dem TIFF-Bild des richtig rotierten PDFs
        ocrkit.create_searchable_pdf(
            tiff_image=tiff_image_correct_rotated,
            out_filename=os.path.join(
                file_output_folder, f"tiff_image_correct_rotated.pdf"
            ),
            language="deu+eng+chi_sim",
        )

        # Erzeugen eines durchsuchbaren PDFs aus dem TIFF-Bild des falsch rotierten PDFs
        ocrkit.create_searchable_pdf(
            tiff_image=tiff_image_wrong_rotated,
            out_filename=os.path.join(
                file_output_folder, f"tiff_image_wrong_rotated.pdf"
            ),
            language="deu+eng+chi_sim",
        )
else:
    print("Ordner müssen gleiche Länge haben")
