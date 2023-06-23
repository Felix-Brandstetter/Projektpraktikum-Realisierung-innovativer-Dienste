import os
from wand.image import Image
from tempfile import TemporaryDirectory
import glob
import ocrkit
from langdetect import detect, detect_langs
import pandas as pd
from ocrkit.language_identification_model import Language_Identification_Model
from ocrkit.unpaper import clean
from pathlib import Path
import subprocess


class TiffImage:
    def __init__(
        self, path: str, workfolder: TemporaryDirectory, dpi: int = 300
    ) -> None:
        self.path = path
        self.workfolder = workfolder
        self.basename = os.path.basename(self.path).split(".")[0]
        self.multipage = self.is_multipage()
        self.dpi = dpi

    def is_multipage(self) -> bool:
        is_multipage = False
        with Image(filename=self.path) as img:
            if len(img.sequence) > 1:
                is_multipage = True
        return is_multipage

    def detect_language(self):
        languages_in_document = pd.DataFrame(columns=["Sprache"])
        tiff_image_ocrdata = ocrkit.get_ocr_data(
            tiff_image=self, language="deu+eng+chi_sim"
        )
        tiff_image_ocrdata = tiff_image_ocrdata[tiff_image_ocrdata["conf"] >= 96]
        page_numbers = list(tiff_image_ocrdata["page_num"].unique())
        page_numbers.append("Whole Document")
        for page in page_numbers:
            counter_deu = 0
            counter_eng = 0
            counter_chi_sim = 0
            if page != "Whole Document":
                ocrdata_per_page = tiff_image_ocrdata[
                    tiff_image_ocrdata["page_num"] == page
                ]
            else:
                ocrdata_per_page = tiff_image_ocrdata
            for index1 in range(len(ocrdata_per_page)):
                row = ocrdata_per_page.iloc[index1]
                word_in_row = row["text"]
                try:
                    lang_word = detect(word_in_row)
                    # print(lang_word)
                except:
                    lang_word = None
                if lang_word == "en":
                    counter_eng += 1
                elif lang_word == "de":
                    counter_deu += 1
                elif lang_word == "zh-cn":
                    counter_chi_sim += 1
            language_in_text = ""
            if counter_eng >= 15:
                language_in_text += " eng "
            if counter_deu >= 15:
                language_in_text += " deu "
            if counter_chi_sim >= 15:
                language_in_text += " chi_sim "
            if language_in_text == "":
                language_in_text = "N/A"
            new_row = {"Sprache": language_in_text}
            new_row = pd.DataFrame(new_row, index=[page])
            languages_in_document = pd.concat(
                [languages_in_document, new_row], axis=0, ignore_index=True
            )
        print(languages_in_document)
        return languages_in_document

    def detect_language2(self):
        languages_in_document = pd.DataFrame(columns=["Sprache"])
        tiff_image_ocrdata = ocrkit.get_ocr_data(
            tiff_image=self, language="deu+eng+chi_sim"
        )
        tiff_image_ocrdata = tiff_image_ocrdata[tiff_image_ocrdata["conf"] >= 96]
        page_numbers = list(tiff_image_ocrdata["page_num"].unique())
        page_numbers.append("Whole Document")
        for page in page_numbers:
            text_in_page = ""
            if page != "Whole Document":
                ocrdata_per_page = tiff_image_ocrdata[
                    tiff_image_ocrdata["page_num"] == page
                ]
            else:
                ocrdata_per_page = tiff_image_ocrdata
            for index1 in range(len(ocrdata_per_page)):
                row = ocrdata_per_page.iloc[index1]
                word_in_row = row["text"]
                text_in_page += " " + word_in_row + " "
            language_identification_model = Language_Identification_Model()
            most_probable_languages = language_identification_model.predict_lang(
                text_in_page
            )
            print(most_probable_languages)
            # new_row = {"Sprache": language_in_text}
            # new_row = pd.DataFrame(new_row, index=[page])
            # languages_in_document = pd.concat([languages_in_document, new_row], axis=0, ignore_index=True)
        # print(languages_in_document)
        return languages_in_document

    def detect_language3(self):
        languages_in_document = pd.DataFrame(columns=["Sprache"])
        tiff_image_ocrdata = ocrkit.get_ocr_data(
            tiff_image=self, language="deu+eng+chi_sim"
        )
        tiff_image_ocrdata = tiff_image_ocrdata[tiff_image_ocrdata["conf"] >= 96]
        page_numbers = list(tiff_image_ocrdata["page_num"].unique())
        page_numbers.append("Whole Document")
        for page in page_numbers:
            text_in_page = ""
            if page != "Whole Document":
                ocrdata_per_page = tiff_image_ocrdata[
                    tiff_image_ocrdata["page_num"] == page
                ]
            else:
                ocrdata_per_page = tiff_image_ocrdata
            for index1 in range(len(ocrdata_per_page)):
                row = ocrdata_per_page.iloc[index1]
                word_in_row = row["text"]
                text_in_page += " " + word_in_row + " "
            detected_languages = detect_langs(text_in_page)
            # Sort the detected languages by probability in descending order
            detected_languages.sort(key=lambda x: x.prob, reverse=True)
            # Get the three most probable languages
            most_probable_languages = detected_languages[:2]
            for language in most_probable_languages:
                print(f"Language: {language.lang}, Probability: {language.prob}")
            # new_row = {"Sprache": language_in_text}
            # new_row = pd.DataFrame(new_row, index=[page])
            # languages_in_document = pd.concat([languages_in_document, new_row], axis=0, ignore_index=True)
        # print(languages_in_document)
        return most_probable_languages

    """ 
    Also known as Local Adaptive Threshold, each pixel value is adjusted by the surrounding pixels. 
    If the current pixel has greater value than the average of the surrounding pixels, then the pixel becomes white, else black.
    """ 
    def binarize_adaptive_threshold(self, width: int = 16, heigth: int = 16):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.adaptive_threshold(
                        width=width, height=heigth  # The size of the surrounding pixels
                    )

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def binarize_auto_threshold(self, method: str = "kapur"):
        if method not in ["kapur", "otsu", "triagle"]:
            print("Not a valid Threshold Method")
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.auto_threshold(method=method)

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def binarize_black(self, method: str = "kapur"):
        if method not in ["kapur", "otsu", "triagle"]:
            print("Not a valid Threshold Method")
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.auto_threshold(method=method)

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_edge(self, radius: int = 1):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.edge(radius=radius)

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def sharpening_emboss(self, radius: int = 3, sigma: int = 1.75):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.emboss(radius, sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_kuwahara(self, radius: int = 2, sigma: int = 1.5):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.kuwahara(radius, sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_shade(self, grey: bool = True, azimuth: int = 286, elevation: int = 45):
            workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
            path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
            with Image(filename=self.path, resolution=self.dpi) as img:
                for page_number in range(len(img.sequence)):
                    with img.sequence[page_number] as page:
                        page.shade(grey, azimuth, elevation)
                img.save(filename=path_to_tiff)
            tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
            return tiff_image
    
    def sharpening_sharpen(self, radius: int = 8, sigma: int = 4):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.sharpen(radius=radius, sigma=sigma)

            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def sharpening_adaptive_sharpen(self, radius: int = 8, sigma: int = 4):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.adaptive_sharpen(radius=radius, sigma=sigma)

            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def deskew(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.deskew(0.4 * img.quantum_range)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def despeckle(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.despeckle()

            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def unpaper_clean(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        tiff_pages = self.split_tiff_image()
        for pagenumber, tiff_page in enumerate(tiff_pages):
            path_to_tiff = os.path.join(
                workfolder.name, self.basename + "{}.tiff".format(pagenumber)
            )
            clean(
                input_file=Path(tiff_page), output_file=Path(path_to_tiff), dpi=self.dpi
            )
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def save_image(self, filename):
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.save(filename=filename)

    def rotate_image_to_corrected_text_orientation(self):
        # TODO Test if that works with multipage
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        pages = self.split_tiff_image()
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number, page in enumerate(pages):
                angle = ocrkit.get_rotation_angle(page)
                if angle != 0.0:
                    print("Rotate page: {} {} degree".format(page_number, angle))
                    with img.sequence[page_number] as img_page:
                        img_page.rotate(angle)

            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def split_tiff_image(self):
        # Split preprocessed_tiff_image in seperated pages
        # TODO in Funktion
        with Image(filename=self.path) as img:
            img.save(
                filename=os.path.join(
                    self.workfolder.name, self.basename + "-page_%00000d.tif"
                )
            )
        files = glob.glob(
            os.path.join(self.workfolder.name, self.basename + "-page_*.tif")
        )

        tiff_pages = []
        for file in files:
            tiff_image = TiffImage(path=file, workfolder=self.workfolder)
            tiff_pages.append(tiff_image)
        return tiff_pages

    # Resize to fit A4 Page. 3508 pixel correspond to large size of A4 page
    def resize_only_shrink_larger_images(self, width: int = 3508, height: int = 3508):
        # TODO TRY CATCH + TIMEOUT
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        command = ["magick", self.path, "-resize", f"{width}x{height}>", path_to_tiff]
        subprocess.run(command, check=True)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
        # Resize to fit A4 Page. 3508 pixel correspond to large size of A4 page
    def resize(self, width: int = 3508, height: int = 3508):
        # TODO TRY CATCH + TIMEOUT
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        command = ["magick", self.path, "-resize", f"{width}x{height}", path_to_tiff]
        subprocess.run(command, check=True)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
