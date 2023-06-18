import tempfile
import os
from wand.image import Image
from ocrkit.tiff_image import TiffImage
import subprocess

class InputPDF:
    def __init__(self, path: str) -> None:
        self.path = path
        self.basename = os.path.basename(self.path).split(".")[0]

    def convert_to_tiff(self) -> TiffImage:
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def convert_to_tiff_with_ghostscript(self) -> TiffImage:
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        args = "gs -dNOPAUSE -r300 -sDEVICE=tiffscaled24 -sCompression=lzw -dBATCH -sOutputFile='{}' '{}'".format(path_to_tiff,self.path)
        subprocess.call(args, shell=True)
        
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image


    
