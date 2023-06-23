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

# Define input folder
input_folder = "/RIDSS2023/src/Experimente/Testdateien"

# Create output folder
output_folder = "/RIDSS2023/experiment_ergebnisse/Skalierung&Auflösung/Resize_Test"
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

