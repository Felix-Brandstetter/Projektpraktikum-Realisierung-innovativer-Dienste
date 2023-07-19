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


from ocrmypdf._pipeline import get_page_square_dpi, get_orientation_correction
# Remove this workaround when we require Pillow >= 10
try:
    BICUBIC = Image.Resampling.BICUBIC  # type: ignore
except AttributeError:  # pragma: no cover
    # Pillow 9 shim
    BICUBIC = Image.BICUBIC  # type: ignore

log = logging.getLogger(__name__)

class Language_Identification_Model:

    def __init__(self, path_to_weights:str = "config/Language_Model_Weights.bin"):
        pretrained_lang_model = path_to_weights
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text, number_of_languages_to_detect, confidence_threshold):
        predictions = self.model.predict(text, k=number_of_languages_to_detect) 
        log.debug(predictions)
        filtered_predictions = [self.map_to_tesseract_label(label) for label, confidence in zip(predictions[0], predictions[1]) if confidence >= confidence_threshold]
        return filtered_predictions
    
    def map_to_tesseract_label(self, label):
        language_mapping = {
            '__label__de': 'deu',
            '__label__en': 'eng',
            '__label__fr': 'fra',
            '__label__es': 'spa',
            '__label__it': 'ita',
            '__label__pt': 'por',
            '__label__nl': 'nld',
            '__label__pl': 'pol',
            '__label__sv': 'swe',
            '__label__da': 'dan',
            '__label__fi': 'fin',
            '__label__hu': 'hun',
            '__label__cs': 'ces',
            '__label__ro': 'ron',
            '__label__tr': 'tur',
            '__label__ru': 'rus',
            '__label__ar': 'ara',
            '__label__zh': 'chi_sim', 
            '__label__ja': 'jpn',
            '__label__ko': 'kor',
            '__label__hi': 'hin',  
            '__label__da': 'dan',  
            '__label__fi': 'fin', 
            '__label__ar': 'ara'  
        }
        
        return language_mapping.get(label, None)


