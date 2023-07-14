from __future__ import annotations
import logging
from pathlib import Path
from ocrmypdf._jobcontext import PageContext, PdfContext
from PIL import Image, ImageColor, ImageDraw
import yaml


from ocrmypdf._pipeline import get_page_square_dpi
# Remove this workaround when we require Pillow >= 10
try:
    BICUBIC = Image.Resampling.BICUBIC  # type: ignore
except AttributeError:  # pragma: no cover
    # Pillow 9 shim
    BICUBIC = Image.BICUBIC  # type: ignore

log = logging.getLogger(__name__)

def read_config(config_file: Path) -> dict:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

config_file = Path('Preprocessing_Ridss2023_Config.yaml')
config = read_config(config_file)

def preprocess_deskew(input_file: Path, page_context: PageContext) -> Path:
    output_file = page_context.get_path('pp_deskew.png')
    dpi = get_page_square_dpi(page_context.pageinfo, page_context.options)

    ocr_engine = page_context.plugin_manager.hook.get_ocr_engine()
    deskew_angle_degrees = ocr_engine.get_deskew(input_file, page_context.options)

    with Image.open(input_file) as im:
        # According to Pillow docs, .rotate() will automatically use Image.NEAREST
        # resampling if image is mode '1' or 'P'
        deskewed = im.rotate(
            deskew_angle_degrees,
            resample=BICUBIC,
            fillcolor=ImageColor.getcolor('white', mode=im.mode),  # type: ignore
        )
        deskewed.save(output_file, dpi=dpi)

    return output_file
