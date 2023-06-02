import tempfile
import os
from wand.image import Image
from ocrkit.tiff_image import TiffImage

class InputPDF:
    def __init__(self, path: str) -> None:
        self.path = path
        self.workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        self.basename = os.path.basename(self.path).split(".")[0]

    def convert_to_tiff(self) -> TiffImage:
        path_to_tiff = os.path.join(self.workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=self.workfolder)
        return tiff_image

    
