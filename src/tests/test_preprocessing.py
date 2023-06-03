from ocrkit import InputPDF
from wand.image import Image


class TestPreprocessing:
    def test_binarize_adaptive_threshold(self):
        # Create new InputPDF
        inputpdf = InputPDF(
            "src/tests/test_ressources/test_binarize_adaptive_threshold/test_image.pdf"
        )

        # Convert to Tiff Image
        tiff_image = inputpdf.convert_to_tiff()

        # Preprocessing
        tiff_image_preprocessed = tiff_image.binarize_adaptive_threshold()

        # Compare Output
        with Image(
            filename="src/tests/test_ressources/test_binarize_adaptive_threshold/controll_image.tiff"
        ) as control_image:
            with Image(filename=tiff_image_preprocessed.path) as converted_image:
                diff_img, diff_val = converted_image.compare(
                    control_image, "root_mean_square"
                )
                print(diff_val)
                assert diff_val == 0
    
    def test_deskew(self):
        # Create new InputPDF
        inputpdf = InputPDF(
            "src/tests/test_ressources/test_deskew/test_image.pdf"
        )

        # Convert to Tiff Image
        tiff_image = inputpdf.convert_to_tiff()

        # Preprocessing
        tiff_image_preprocessed = tiff_image.deskew()

        # Compare Output
        with Image(
            filename="/RIDSS2023/src/tests/test_ressources/test_deskew/controll_image.tiff"
        ) as control_image:
            with Image(filename=tiff_image_preprocessed.path) as converted_image:
                diff_img, diff_val = converted_image.compare(
                    control_image, "root_mean_square"
                )
                print(diff_val)
                assert diff_val == 0

