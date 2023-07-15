from __future__ import annotations
import logging
from pathlib import Path
from ocrmypdf._jobcontext import PageContext
from PIL import Image, ImageColor
import yaml
import numpy as np
from deskew import determine_skew
from wand.image import Image as WandImage
import io
import fasttext
from ocrmypdf.language_detection import Language_Identification_Model
import pytesseract


from ocrmypdf._pipeline import get_page_square_dpi, get_orientation_correction

# Remove this workaround when we require Pillow >= 10
try:
    BICUBIC = Image.Resampling.BICUBIC  # type: ignore
except AttributeError:  # pragma: no cover
    # Pillow 9 shim
    BICUBIC = Image.BICUBIC  # type: ignore

log = logging.getLogger(__name__)


def read_config(config_file: Path) -> dict:
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


config_file = Path("config/Preprocessing_Ridss2023_Config.yaml")
config = read_config(config_file)


def preprocess_deskew_ridss2023(input_file: Path, page_context: PageContext) -> Path:
    """
    Deskews an image and saves the result.

    Args:
        input_file (Path): The path to the input image file.
        page_context (PageContext): The context of the page containing the image.

    Returns:
        Path: The path to the output image file after deskewing.
    """
    output_file = page_context.get_path("pp_deskew.png")
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)

    # Graustufenbild erzeugen
    with Image.open(input_file) as im:
        grayscale = im.convert("L")

        deskew_angle_degrees = determine_skew(np.array(grayscale))

        # Restlicher Code ...
        with im.rotate(
            deskew_angle_degrees,
            resample=BICUBIC,
            fillcolor=ImageColor.getcolor("white", mode=im.mode),
        ) as deskewed:
            deskewed.save(output_file, dpi=dpi)
    log.info(f"Deskewridss2023 finished succesfully: Angle:  {deskew_angle_degrees}")
    return output_file


def preprocess_rotate_image_to_corrected_text_orientation_ridss2023(
    input_file: Path, page_context: PageContext
) -> Path:
    """
    Rotates an image to correct its text orientation and saves the result.

    Args:
        input_file (Path): The path to the input image file.
        page_context (PageContext): The context of the page containing the image.

    Returns:
        Path: The path to the output image file with corrected text orientation.

    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    output_file = page_context.get_path("rotate_image_to_correct_text_orientation.png")
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)
    angle = get_orientation_correction(input_file, page_context)
    with Image.open(input_file) as im:
        deskewed = im.rotate(
            angle,
            resample=BICUBIC,
            fillcolor=ImageColor.getcolor("white", mode=im.mode),
        )
    deskewed.save(output_file, dpi=dpi)
    log.info(
        f"Rotate image to corrected text_orientation finished succesfully: Angle: {angle}"
    )
    return output_file


def preprocess_normalize_contrast_ridss2023(
    input_file: Path, page_context: PageContext
) -> Path:
    """
    Normalizes the contrast of an image and saves the result.
    For more Information see: https://imagemagick.org/script/command-line-options.php#normalize

    Args:
        input_file (Path): The path to the input image file.
        page_context (PageContext): The context of the page containing the image.

    Returns:
        Path: The path to the output image file with normalized contrast.
    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    output_file = page_context.get_path("preprocess_normalize_contrast_ridss2023.png")
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)
    dpi_int = dpi.x
    with WandImage(filename=str(input_file), resolution=(dpi.x, dpi.y)) as wand_image:
        wand_image.normalize()
        pillow_image = Image.open(
            io.BytesIO(
                np.asarray(bytearray(wand_image.make_blob(format="png")), dtype="uint8")
            )
        )

        # Speichern des Pillow-Images mit DPI-Tag
        pillow_image.save(output_file, dpi=dpi)
    log.info(f"Normalize Contrast finished succesfully")
    return output_file


def preprocess_autolevel_contrast_ridss2023(
    input_file: Path, page_context: PageContext
) -> Path:
    """
    Adjusts the contrast of an image using auto-leveling and saves the result.
    For more Information see: <https://imagemagick.org/script/command-line-options.php#auto-level>

    Args:
        input_file (Path): The path to the input image file.
        page_context (PageContext): The context of the page containing the image.

    Returns:
        Path: The path to the output image file with adjusted contrast.
    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    output_file = page_context.get_path("preprocess_autolevel_contrast_ridss2023.png")
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)
    dpi_int = dpi.x
    with WandImage(filename=str(input_file), resolution=(dpi.x, dpi.y)) as wand_image:
        wand_image.auto_level()
        pillow_image = Image.open(
            io.BytesIO(
                np.asarray(bytearray(wand_image.make_blob(format="png")), dtype="uint8")
            )
        )

        # Speichern des Pillow-Images mit DPI-Tag
        pillow_image.save(output_file, dpi=dpi)
    log.info(f"Autolevel contrast finished succesfully")
    return output_file


def preprocess_improve_contrast_ridss2023(
    input_file: Path, page_context: PageContext
) -> Path:
    """
    Adjusts the contrast of an image using contrast and saves the result.
    For more Information see: <https://imagemagick.org/script/command-line-options.php#contrast>

    Args:
        input_file (Path): The path to the input image file.
        page_context (PageContext): The context of the page containing the image.

    Returns:
        Path: The path to the output image file with adjusted contrast.
    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    output_file = page_context.get_path("preprocess_improve_contrast_ridss2023.png")
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)
    dpi_int = dpi.x
    with WandImage(filename=str(input_file), resolution=(dpi.x, dpi.y)) as wand_image:
        wand_image.contrast()
        pillow_image = Image.open(
            io.BytesIO(
                np.asarray(bytearray(wand_image.make_blob(format="png")), dtype="uint8")
            )
        )

        # Speichern des Pillow-Images mit DPI-Tag
        pillow_image.save(output_file, dpi=dpi)
    log.info(f"Improve contrast finished succesfully")
    return output_file


def preprocess_sharpen_edges_ridss2023(input_file: Path, page_context: PageContext):
    """
    Adjusts the contrast of an image using contrast and saves the result.
    For more Information see: <https://imagemagick.org/script/command-line-options.php#sharpen>

    Args:
        input_file (Path): The path to the input image file.
        page_context (PageContext): The context of the page containing the image.

    Returns:
        Path: The path to the output image file with adjusted contrast.

    Configurations:
        - radius (float): The radius parameter for the sharpening function. Can be configured in the YAML file.
        - sigma (float): The sigma parameter for the sharpening function. Can be configured in the YAML file.

    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    output_file = page_context.get_path("preprocess_sharpen_edges_ridss2023.png")
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)
    dpi_int = dpi.x

    radius = config.get("preprocess_sharpen_edges_ridss2023", {}).get("radius", 1.0)
    sigma = config.get("preprocess_sharpen_edges_ridss2023", {}).get("sigma", 0.5)

    with WandImage(filename=str(input_file), resolution=(dpi.x, dpi.y)) as wand_image:
        wand_image.sharpen(radius=radius, sigma=sigma)
        pillow_image = Image.open(
            io.BytesIO(
                np.asarray(bytearray(wand_image.make_blob(format="png")), dtype="uint8")
            )
        )

        # Speichern des Pillow-Images mit DPI-Tag
        pillow_image.save(output_file, dpi=dpi)
    log.info(f"Image contrast was increased with auto-level")
    return output_file


def preprocess_auto_language_detection(input_file: Path, page_context: PageContext):
    path_to_weights = config.get("preprocess_detect_languages", {}).get(
        "path_to_weights"
    )
    number_of_languages_to_detect = config.get("preprocess_detect_languages", {}).get(
        "number_of_languages_to_detect", 2
    )
    confidence_threshold = config.get("preprocess_detect_languages", {}).get(
        "confidence_threshold", 0.5
    )
    default_languages = config.get("preprocess_detect_languages", {}).get(
        "default_languages", "eng+deu+chi_sim"
    )
    
    text = pytesseract.image_to_string(str(input_file), lang=default_languages)
    text = text.replace('\n', ' ')
    model = Language_Identification_Model(path_to_weights=path_to_weights)
    detected_languages = model.predict_lang(text, number_of_languages_to_detect, confidence_threshold)
    log.info("Languages: {detected_languages} were detected in document with confidences over : {confidence_threshold}")
    existing_languages = page_context.options.languages
    existing_languages.update(detected_languages)

def preprocess_dewarp_ridss2023(input_file: Path, page_context: PageContext):
    # TODO
    """
    Currently not implemented

    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    log.warning(f"--dewarp option is currently not implemented")
    return input_file


def preprocess_multi_angle_deskew_ridss2023(
    input_file: Path, page_context: PageContext
):
    # TODO
    """
    Currently not implemented

    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    log.warning(f"--multi-angle-deskew option is currently not implemented")
    return input_file


def preprocess_remove_borders_ridss2023(input_file: Path, page_context: PageContext):
    # TODO
    """
    Currently not implemented

    See Also:
        - :func:`ocrmypdf._sync.preprocess`
    """
    log.warning(f"--remove-borders option is currently not implemented")
    return input_file
