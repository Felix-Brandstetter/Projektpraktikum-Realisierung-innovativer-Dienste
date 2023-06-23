import tempfile
import os
from wand.image import Image
from ocrkit.tiff_image import TiffImage
import subprocess
import shutil


class InputPDF:
    def __init__(
        self, path: str, workfolder: tempfile.TemporaryDirectory = None
    ) -> None:
        self.path = path
        self.basename = os.path.basename(self.path).split(".")[0]
        self.workfolder = workfolder

    def convert_to_tiff(self) -> TiffImage:
        # TOD resize to a4
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def convert_to_tiff_with_ghostscript(
        # TOD resize to a4
        self,
        dpi: int = 300,
        auto_rotate_pages: bool = True,
    ):
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        gs_command = [
            "gs",
            "-dNOPAUSE",
            "-r{}".format(dpi),
            "-dBATCH",
            "-sCompression=lzw",
            "-dSAFER",
            "-sDEVICE=tiffscaled24",
            "-sOutputFile=" + path_to_tiff,
            self.path,
        ]
        if auto_rotate_pages:
            gs_command.insert(-2, "-dAutoRotatePages=/PageByPage")
        subprocess.call(gs_command)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image


    def convert_to_tiff_with_imagemagick(
        self,
        dpi: int = 300,
        auto_rotate_pages: bool = True,
        width: int = 0,
        height: int = 0
    ):
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        magick_command = [
            "magick",
            "-density",
            "{}".format(dpi),
            self.path,
            "-compress",
            "LZW",
            self.path
        ]
        if auto_rotate_pages:
            magick_command.append("-auto-rotate")
        if width != 0 and height != 0:
            magick_command.extend(["-resize", "{}x{}>".format(width, height)])

        magick_command.append(path_to_tiff)

        subprocess.call(magick_command)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def save_pdf(self, filename):
        shutil.copyfile(self.path, filename)
