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

        
# Pfad zum Eingabeordner mit den PDF-Dateien
input_folder = "/RIDSS2023/src/Experimente/Testdateien"

output_folder = "/RIDSS2023/experiment_ergebnisse/Sprache/Language_Test"
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

languages = ["eng", "deu", "chi_sim","deu+eng+chi_sim","ita+ara+fin+dan+fra+hin+spa+por+deu+eng+chi_sim","eng+chi_sim","eng+deu"]  # Liste der zu verwendenden Sprachen
# Überprüfen und Erstellen des Ausgabeverzeichnisses
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

# Schleife über alle Dateien im Eingabeverzeichnis
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        # Pfad zur aktuellen Eingabedatei
        input_file = os.path.join(input_folder, filename)
        
        # Erstellen des InputPDF-Objekts
        inputpdf = ocrkit.InputPDF(input_file)

        # Erzeuge den Ausgabepfad für die aktuellen Datei
        file_output_folder = os.path.join(output_folder, filename[:-4])

        # Lösche den Ausgabeordner, falls er bereits existiert
        if os.path.exists(file_output_folder):
            shutil.rmtree(file_output_folder)

        # Erstelle den Ausgabeordner
        os.makedirs(file_output_folder)
        
        # Konvertieren in Tiff-Bild
        tiff_image = inputpdf.convert_to_tiff_with_ghostscript(dpi=300)
        tiff_image.save_image(os.path.join(file_output_folder, "tiff_image_300_dpi.tiff"))
        
        runtimes = []

        # Schleife über die Sprachen
        for language in languages:
            # Ausführen des OCR-Codes und Zeitmessung
            start_time = datetime.now()
            ocrdata = ocrkit.get_ocr_data(delete_minus1_confidences=False, tiff_image=tiff_image, language=language)
            runtime = datetime.now() - start_time
            runtimes.append("Laufzeit für {} Sprache:{} \n".format(language,runtime))
            # Auswerten der OCR-Daten
            evaluation_ocrdata = utils.evaluate_ocrdata(ocrdata)
            evaluation_ocrdata.to_excel(os.path.join(file_output_folder, f"evaluation_ocrdata_{language}.xlsx"))
                        # Create searchable PDF
            ocrkit.create_searchable_pdf(
                tiff_image=tiff_image,
                out_filename=os.path.join(file_output_folder, f"tiff_image_{language}.pdf"),
                language="{}".format(language),
            )

        with open(os.path.join(file_output_folder, "Tesseract_Laufzeiten.txt"), "w") as f:
            f.write(" ".join(runtimes))
