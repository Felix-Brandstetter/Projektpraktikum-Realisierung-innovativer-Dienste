import os
from wand.image import Image
from tempfile import TemporaryDirectory
import glob
import ocrkit
from langdetect import detect, detect_langs
import pandas as pd
from ocrkit.language_identification_model import Language_Identification_Model
from ocrkit.unpaper import clean
import subprocess
from pathlib import Path
import cv2
from skimage.morphology import skeletonize, medial_axis, thin
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
        """"
        Check if the TIFF image contains multiple pages
        """
        # Set the initial value of the 'is_multipage' flag to False
        is_multipage = False
        # Open the TIFF image using the 'Image' class from the 'wand' library
        with Image(filename=self.path) as img:
            # Check if the image has more than one page (sequence)
            if len(img.sequence) > 1:
                # If the image has more than one page, set the 'is_multipage' flag to True
                is_multipage = True
        # Return the value of the 'is_multipage' flag
        return is_multipage
    
    def save_image(self, filename):
        """
        Saves the TIFF image as a separate file with the specified filename
        """
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.save(filename=filename)

    def split_tiff_image(self):
        """ Split preprocessed_tiff_image into separate pages"""

        # Save the preprocessed_tiff_image as individual pages
        with Image(filename=self.path) as img:
            img.save(
                filename=os.path.join(
                    self.workfolder.name, self.basename + "-page_%00000d.tif"
                )
            )
        # Get the list of file paths for the individual pages
        files = glob.glob(
            os.path.join(self.workfolder.name, self.basename + "-page_*.tif")
        )
        tiff_pages = []
        for file in files:
            # Create TiffImage objects for each page
            tiff_image = TiffImage(path=file, workfolder=self.workfolder)
            tiff_pages.append(tiff_image)
        return tiff_pages


    def detect_language(self):
        """
        Detect the languages used in each page
        """

        # Create an empty DataFrame to store the detected languages
        languages_in_document = pd.DataFrame(columns=["Sprache"])
        # Get the OCR data for the TIFF image using the 'ocrkit.get_ocr_data' function
        tiff_image_ocrdata = ocrkit.get_ocr_data(tiff_image=self, language="deu+eng+chi_sim")
        # Filter the OCR data based on confidence level
        tiff_image_ocrdata = tiff_image_ocrdata[tiff_image_ocrdata["conf"] >= 96]
        # Get the unique page numbers in the OCR data
        page_numbers = list(tiff_image_ocrdata["page_num"].unique())
        # Add "Whole Document" as a page number
        page_numbers.append("Whole Document")
        # Iterate over the page numbers
        for page in page_numbers:
            # Initialize counters for different languages
            counter_deu = 0
            counter_eng = 0
            counter_chi_sim = 0
            # Filter the OCR data based on the current page number
            if page != "Whole Document":
                ocrdata_per_page = tiff_image_ocrdata[tiff_image_ocrdata["page_num"] == page]
            else:
                ocrdata_per_page = tiff_image_ocrdata
            # Iterate over the OCR data rows for the current page
            for index1 in range(len(ocrdata_per_page)):
                # Get the text from the current OCR data row
                row = ocrdata_per_page.iloc[index1]
                word_in_row = row["text"]
                try:
                    # Perform language detection on the word using the 'detect' function
                    lang_word = detect(word_in_row)
                except:
                    # Handle any errors that occur during language detection
                    lang_word = None
                # Increment the respective language counter based on the detected language
                if lang_word == "en":
                    counter_eng += 1
                elif lang_word == "de":
                    counter_deu += 1
                elif lang_word == "zh-cn":
                    counter_chi_sim += 1
            # Include the language in language_in_text if more than 
            # a certain amount of words are detected in that language
            language_in_text = ""
            if counter_eng >= 15:
                language_in_text += " eng "
            if counter_deu >= 15:
                language_in_text += " deu "
            if counter_chi_sim >= 15:
                language_in_text += " chi_sim "
            if language_in_text == "":
                language_in_text = "N/A"
            # Create a new row with the detected languages and append it to the DataFrame
            new_row = {"Sprache": language_in_text}
            new_row = pd.DataFrame(new_row, index=[page])
            languages_in_document = pd.concat(
                [languages_in_document, new_row], axis=0, ignore_index=True
            )
        # Print the DataFrame containing the detected languages
        print(languages_in_document)
        # Return the DataFrame with the detected languages
        return languages_in_document

    def detect_language2(self):
        """
        Detect the languages used in each page
        """

        # Get the OCR data for the TIFF image using the 'ocrkit.get_ocr_data' function
        tiff_image_ocrdata = ocrkit.get_ocr_data(tiff_image=self, language="deu+eng+chi_sim")
        # Filter the OCR data based on confidence level
        tiff_image_ocrdata = tiff_image_ocrdata[tiff_image_ocrdata["conf"] >= 96]
        # Get the unique page numbers in the OCR data
        page_numbers = list(tiff_image_ocrdata["page_num"].unique())
        # Add "Whole Document" as a page number
        page_numbers.append("Whole Document")
        # Iterate over the page numbers
        for page in page_numbers:
            # Initialize an empty string to store the text in the page
            text_in_page = ""
            # Filter the OCR data based on the current page number
            if page != "Whole Document":
                ocrdata_per_page = tiff_image_ocrdata[tiff_image_ocrdata["page_num"] == page]
            else:
                ocrdata_per_page = tiff_image_ocrdata
            # Iterate over the OCR data rows for the current page
            for index1 in range(len(ocrdata_per_page)):
                # Get the text from the current OCR data row
                row = ocrdata_per_page.iloc[index1]
                word_in_row = row["text"]
                # Concatenate the word to the text in the page string
                text_in_page += " " + word_in_row + " "
            # Create an instance of the Language_Identification_Model class
            language_identification_model = Language_Identification_Model()
            # Use the language identification model to predict the most probable languages in the page text
            most_probable_languages = language_identification_model.predict_lang(text_in_page)
        # Return the most probable languages
        return most_probable_languages

    def detect_language3(self):
        """
        Detect the languages used in each page
        """

        # Get the OCR data for the TIFF image using the 'ocrkit.get_ocr_data' function
        tiff_image_ocrdata = ocrkit.get_ocr_data(tiff_image=self, language="deu+eng+chi_sim")
        # Filter the OCR data based on confidence level
        tiff_image_ocrdata = tiff_image_ocrdata[tiff_image_ocrdata["conf"] >= 96]
        # Get the unique page numbers in the OCR data
        page_numbers = list(tiff_image_ocrdata["page_num"].unique())
        # Add "Whole Document" as a page number
        page_numbers.append("Whole Document")
        # Iterate over the page numbers
        for page in page_numbers:
            # Initialize an empty string to store the text in the page
            text_in_page = ""
            # Filter the OCR data based on the current page number
            if page != "Whole Document":
                ocrdata_per_page = tiff_image_ocrdata[tiff_image_ocrdata["page_num"] == page]
            else:
                ocrdata_per_page = tiff_image_ocrdata
            # Iterate over the OCR data rows for the current page
            for index1 in range(len(ocrdata_per_page)):
                # Get the text from the current OCR data row
                row = ocrdata_per_page.iloc[index1]
                word_in_row = row["text"]
                # Concatenate the word to the text in the page string
                text_in_page += " " + word_in_row + " "
            # Use the 'detect_langs' function to detect the languages in the page text
            detected_languages = detect_langs(text_in_page)
            # Sort the detected languages by probability in descending order
            detected_languages.sort(key=lambda x: x.prob, reverse=True)
            # Get the three most probable languages
            most_probable_languages = detected_languages[:2]
            # Print the detected languages and their probabilities
            for language in most_probable_languages:
                print(f"Language: {language.lang}, Probability: {language.prob}")
        # Return the most probable languages
        return most_probable_languages

    def binarize_adaptive_threshold(self, width: int = 16, height: int = 16):
        """
        Binarize the image using the adaptive threshold method from Wand
        Also known as Local Adaptive Threshold, each pixel value is adjusted by the surrounding pixels. 
        If the current pixel has greater value than the average of the surrounding pixels, then the pixel becomes white, else black.
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.transform_colorspace("gray")
                    page.adaptive_threshold(
                        width=width,
                        height=height,  # The size of the surrounding pixels
                        offset=-0.0000001 * page.quantum_range,
                    )
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def binarize_auto_threshold(self, method: str = "kapur"):
        """
        Binarize the image using the auto threshold method from Wand
        """

        if method not in ["kapur", "otsu", "triagle"]:
            print("Not a valid Threshold Method")
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.transform_colorspace("gray")
            img.auto_threshold(method=method)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def binarize_black_threshold(self, threshold: str = "#930"):
        """
        Binarize the image using the black threshold method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.transform_colorspace("gray")
            img.black_threshold(threshold=threshold)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def binarize_range_threshold(self, threshold: str = "#930"):
        """
        Binarize the image using the range threshold method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.transform_colorspace("gray")
            white_point = 0.9 * img.quantum_range
            black_point = 0.5 * img.quantum_range
            delta = 0.05 * img.quantum_range
            img.range_threshold(
                low_black=black_point - delta,
                low_white=white_point - delta,
                high_white=white_point + delta,
                high_black=black_point + delta,
            )
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_edge(self, radius: int = 1):
        """
        Sharpen the image using the edge method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.transform_colorspace("gray")
            img.edge(radius=radius)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_emboss(self, radius: int = 3, sigma: int = 1.75):
        """
        Sharpen the image using the emboss method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.transform_colorspace("gray")
            img.emboss(radius=radius, sigma=sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_kuwahara(self, radius: int = 2, sigma: int = 1.5):
        """
        Sharpen the image using the kuwahara method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.kuwahara(radius=radius, sigma=sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def sharpening_shade(self, gray: bool = True, azimuth: int = 286, elevation: int = 45):
        """
        Sharpen the image using the shade method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.shade(gray=gray, azimuth=azimuth, elevation=elevation)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def sharpening_sharpen(self, radius: int = 8, sigma: int = 4):
        """
        Sharpen the image using the sharpen method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.sharpen(radius=radius, sigma=sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_adaptive_sharpen(self, radius: int = 8, sigma: int = 4):
        """
        Sharpen the image using the adaptive sharpen method from Wand
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.adaptive_sharpen(radius=radius, sigma=sigma)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def sharpening_unsharp_mask(
    self, radius: int = 10, sigma: int = 4, amount: int = 1, threshold: int = 0
    ):
        """
        Sharpen the image using the unsharp mask method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.unsharp_mask(
                radius=radius, sigma=sigma, amount=amount, threshold=threshold
            )
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def skeletonize_zhang(self):
        """
        Skeletonize the image using the zhang method from scikit-image
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Read the tiff image as a grayscale cv2 image
        img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        # Binarize the image
        _, binary_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Invert the colors
        binary_image = invert(binary_image)
        # Skeletonize the inverted cv2 image
        skeleton = skeletonize(binary_image)
        # Invert the skeleton image back to the original
        skeleton = invert(skeleton)
        # Convert the image from binary into type unsigned 8-bit integer with values from 0-255
        skeleton = skeleton.astype(np.uint8) * 255
        # Save the resulting image
        cv2.imwrite(path_to_tiff, skeleton)
        # Save the image as a TiffImage
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def skeletonize_medial_axis(self):
        """
        Skeletonize the image using the medial axis method from scikit-image
        """

        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Read the tiff image as a grayscale cv2 image
        img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        # Binarize the image
        _, binary_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Invert the colors
        binary_image = invert(binary_image)
        # Skeletonize the inverted cv2 image
        skeleton = medial_axis(binary_image)
        # Invert the skeleton image back to the original
        skeleton = invert(skeleton)
        # Convert the image from binary into type unsigned 8-bit integer with values from 0-255
        skeleton = skeleton.astype(np.uint8) * 255
        # Save the resulting image
        cv2.imwrite(path_to_tiff, skeleton)
        # Save the image as a TiffImage
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def skeletonize_thin(self):
        """
        Skeletonize the image using the thin method from scikit-image
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Read the tiff image as a grayscale cv2 image
        img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        # Binarize the image
        _, binary_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Invert the colors
        binary_image = invert(binary_image)
        # Thin the inverted cv2 image
        thinned_img = thin(binary_image, max_num_iter=1)
        # Invert the thinned image back to the original
        thinned_img = invert(thinned_img)
        # Convert the image from binary into type unsigned 8-bit integer with values from 0-255
        thinned_img = thinned_img.astype(np.uint8) * 255
        # Save the resulting image
        cv2.imwrite(path_to_tiff, thinned_img)
        # Save the image as a TiffImage
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def skeletonize_opencv(self):
        """
        Skeletonize the image using openCV
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Read the image as a grayscale image
        img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        # Step 1: Create an empty skeleton
        skeleton = np.zeros(img.shape, np.uint8)
        # Get a Cross Shaped Kernel
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        # Repeat steps 2-4
        while True:
            # Step 2: Open the image
            open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
            # Step 3: Subtract open from the original image
            temp = cv2.subtract(img, open)
            # Step 4: Erode the original image and refine the skeleton
            eroded = cv2.erode(img, element)
            skeleton = cv2.bitwise_or(skeleton, temp)
            img = eroded.copy()
            # Step 5: If there are no white pixels left, i.e., the image has been completely eroded, quit the loop
            if cv2.countNonZero(img) == 0:
                break
        # Invert the skeleton image back to the original
        skeleton = invert(skeleton)
        cv2.imwrite(path_to_tiff, skeleton)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def deskew(self):
        """
        Deskew the image using the deskew method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.deskew(0.4 * img.quantum_range)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def despeckle(self):
        """
        Despeckle the image using the despeckle method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.despeckle()
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def despeckle_opencv(self):
        """
        Despeckle the image using the fastNlMeansDenoising method from openCV
        """
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
        """
        Despeckle the image using the medianBlur method from openCV
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Apply denoising
        im_gray = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        denoised_image = cv2.medianBlur(im_gray, 3)
        # Save denoised image as TIFF
        cv2.imwrite(path_to_tiff, denoised_image)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def turn_gray(self):
        """
        Turn the image gray with the transform colorspace method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.transform_colorspace("gray")
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def contrast_simple_contrast(self):
        """
        Improve the contrast of the image with the contrast method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.contrast(sharpen=True)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def contrast_local_contrast(self, radius=10, strength=12.5):
        """
        Improve the contrast of the image with the local_contrast method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.local_contrast(radius=radius, strength=strength)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def contrast_sigmoidal_contrast(self, strength=3, midpoint=0.65):
        """
        Improve the contrast of the image with the sigmoidal_contrast method from Wand
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=self.dpi) as img:
            img.sigmoidal_contrast(strength=strength, midpoint=midpoint * img.quantum_range)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def clean_unpaper(self):
        """
        Preprocess the image using the clean method from unpaper
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")

        clean(input_file=Path(self.path), output_file=Path(path_to_tiff), dpi=self.dpi)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def rotate_image_to_corrected_text_orientation(self):
        """ 
        Rotate the image to correct the text orientation
        """
        # Create a temporary working folder
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Split the TIFF image into separate pages
        pages = self.split_tiff_image()
        # Open the original TIFF image using wand.image.Image
        with Image(filename=self.path, resolution=self.dpi) as img:
            # Iterate over each page and determine the rotation angle
            for page_number, page in enumerate(pages):
                angle = ocrkit.get_rotation_angle(page)
                if angle != 0.0:
                    print("Rotate page: {} {} degree".format(page_number, angle))
                    # Rotate the corresponding image page in the original TIFF image
                    with img.sequence[page_number] as img_page:
                        img_page.rotate(angle)
            # Save the modified image with corrected orientation
            img.save(filename=path_to_tiff)
        # Create a TiffImage object for the modified TIFF image
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def resize_only_shrink_larger_images(self, width=3508, height=3508):
        """
        Resize the image to fit an A4 page, but only shrink larger images
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        command = ["magick", self.path, "-resize", f"{width}x{height}>", path_to_tiff]
        subprocess.run(command, check=True)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def resize(self, width=3508, height=3508):
        """
        Resize the image to fit an A4 page
        """
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        command = ["magick", self.path, "-resize", f"{width}x{height}", path_to_tiff]
        subprocess.run(command, check=True)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image


