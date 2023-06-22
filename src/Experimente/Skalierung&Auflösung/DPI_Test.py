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

def print_size_of_image(image: TiffImage):
    im = Image.open(image.path)
    width, height = im.size
    print("Width: {}".format(width))
    print("Height: {}".format(height)) 

# Create new InputPDF
inputpdf = InputPDF("/RIDSS2023/inputfolder/4974 Nicolas_ReimannDeLaCruz-13.pdf")


# Pfad zum Eingabeordner mit den PDF-Dateien
input_folder = "/RIDSS2023/src/Experimente/Testdateien"

output_folder = "/RIDSS2023/experiment_ergebnisse/Skalierung&Auflösung/DPI_Test"
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

        # Convert to Tiff Image with different DPIs
        dpi_list = [72, 150, 300, 600, 1200, 2400]
        # Erzeuge eine leere Liste für die Laufzeiten
        runtimes = []
        for dpi in dpi_list:
            startTime = datetime.now()
            tiff_image = inputpdf.convert_to_tiff_with_ghostscript(dpi=dpi)
            runtime = datetime.now() - startTime
            runtimes.append("Laufzeit für {} DPI:{} \n".format(dpi,runtime))
            print(runtime)
            print_size_of_image(tiff_image)
            #Resize Image to fit A4 Page. 3508 pixels correspond to large site of A4 page.
            tiff_image = tiff_image.resize(width=3508, height=3508)
            tiff_image.save_image(
                os.path.join(file_output_folder, f"tiff_image_{dpi}_dpi.tiff")
            )

            # Get ocrdata from Tiff Image
            ocrdata = ocrkit.get_ocr_data(
                tiff_image=tiff_image, language="deu+eng+chi_sim"
            )

            # Get Evaluation Data
            evaluation_ocrdata = utils.evaluate_ocrdata(ocrdata)

            # Save to Excel
            evaluation_ocrdata.to_excel(
                os.path.join(file_output_folder, f"evaluation_ocrdata_{dpi}_dpi.xlsx")
            )

            # Create Searchable PDF
            ocrkit.create_searchable_pdf(
                tiff_image=tiff_image,
                out_filename=os.path.join(
                    file_output_folder, f"tiff_image_{dpi}_dpi.pdf"
                ),
                language="deu+eng+chi_sim",
            )
        with open(os.path.join(file_output_folder, "Ghostscript_Laufzeiten.txt"), "w") as f:
            f.write(" ".join(runtimes))
