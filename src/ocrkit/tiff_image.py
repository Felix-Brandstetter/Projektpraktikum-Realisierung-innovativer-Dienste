import os
from wand.image import Image
from wand.display import display
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt


class TiffImage:
    def __init__(self, path: str, workfolder: TemporaryDirectory) -> None:
        self.path = path
        self.workfolder = workfolder
        self.basename = os.path.basename(self.path).split(".")[0]

    def binarize_adaptive_threshold(self):
        path_to_tiff = os.path.join(self.workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.transform_colorspace("gray")
            img.adaptive_threshold(
                width=16, height=16, offset=-0.08 * img.quantum_range
            )
            img.alpha_channel = "off"
            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=self.workfolder)
        return tiff_image

    def deskew(self):
        path_to_tiff = os.path.join(self.workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.deskew(0.4 * img.quantum_range)
            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=self.workfolder)
        return tiff_image

    def adaptive_sharpen(self):
        path_to_tiff = os.path.join(self.workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.adaptive_sharpen(radius=8, sigma=4)
            img.save(filename="effect-adaptive-sharpen.jpg")

        tiff_image = TiffImage(path=path_to_tiff, workfolder=self.workfolder)
        return tiff_image

    def display(self):
        img = plt.imread(self.path)
        plt.imshow(img)
