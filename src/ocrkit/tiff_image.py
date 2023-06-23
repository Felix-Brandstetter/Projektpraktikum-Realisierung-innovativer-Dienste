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
from ocrkit.unpaper import clean
from pathlib import Path
import cv2
from skimage.morphology import skeletonize
import numpy as np
from skimage.util import invert


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
                        width=width,
                        height=heigth,  # The size of the surrounding pixels
                        offset=-0.0000001 * page.quantum_range,
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

    def binarize_black_threshold(self, threshold: str = "#930"):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.black_threshold(threshold=threshold)

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def binarize_range_threshold(self, threshold: str = "#930"):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    white_point = 0.9 * page.quantum_range
                    black_point = 0.5 * page.quantum_range
                    delta = 0.05 * page.quantum_range
                    page.range_threshold(
                        low_black=black_point - delta,
                        low_white=white_point - delta,
                        high_white=white_point + delta,
                        high_black=black_point + delta,
                    )

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def edge(self, radius: int = 1):
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
                    page.emboss(radius=radius, sigma=sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_kuwahara(self, radius: int = 2, sigma: int = 1.5):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.kuwahara(radius=radius, sigma=sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_shade(
        self, grey: bool = True, azimuth: int = 286, elevation: int = 45
    ):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.shade(grey=grey, azimuth=azimuth, elevation=elevation)
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

    def sharpening_unsharp_mask(
        self, radius: int = 10, sigma: int = 4, amount: int = 1, threshold: int = 0
    ):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.unsharp_mask(
                        radius=radius, sigma=sigma, amount=amount, threshold=threshold
                    )
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def skeletonize_zhang(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")

        # Apply denoising
        im_gray = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        im_gray = invert(im_gray)
        skeleton = skeletonize(im_gray)
        skeleton = skeleton.astype(np.uint8)
        print(skeleton)
        # Save denoised image as TIFF
        cv2.imwrite(path_to_tiff, skeleton)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def skeletonize_opencv(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Read the image as a grayscale image
        img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

        # Step 1: Create an empty skeleton
        skel = np.zeros(img.shape, np.uint8)

        # Get a Cross Shaped Kernel
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        # Repeat steps 2-4
        while True:
            # Step 2: Open the image
            open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
            # Step 3: Substract open from the original image
            temp = cv2.subtract(img, open)
            # Step 4: Erode the original image and refine the skeleton
            eroded = cv2.erode(img, element)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()
            # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
            if cv2.countNonZero(img) == 0:
                break
        cv2.imwrite(path_to_tiff, skel)
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

    def despeckle_opencv(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")

        # Apply denoising
        im_gray = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        denoised_image = cv2.fastNlMeansDenoising(
            im_gray, h=30, templateWindowSize=3, searchWindowSize=3
        )

        # Save denoised image as TIFF
        cv2.imwrite(path_to_tiff, denoised_image)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def blur_opencv(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")

        # Apply denoising
        im_gray = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        denoised_image = cv2.medianBlur(im_gray, 3)

        # Save denoised image as TIFF
        cv2.imwrite(path_to_tiff, denoised_image)

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

    def clean_unpaper(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        clean(input_file=Path(self.path), output_file=Path(path_to_tiff), dpi=self.dpi)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
