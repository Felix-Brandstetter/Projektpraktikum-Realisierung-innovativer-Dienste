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
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"
            img.depth = 8
            img.alpha_channel = "off"
            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def convert_to_tiff_with_ghostscript(self, dpi: int = 300) -> TiffImage:
        workfolder = tempfile.TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        args = "gs -dNOPAUSE -r{} -sDEVICE=tiffscaled24 -sCompression=lzw -dBATCH -sOutputFile='{}' '{}'".format(
            dpi, path_to_tiff, self.path
        )
        subprocess.call(args, shell=True)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    import subprocess

    def convert_pdf_to_tiff(
        self, width: int = None, dpi: int = 300, auto_rotate_pages: bool = True
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
        if width is not None:
            gs_command.insert(-2, "-g{}x".format(width))

        subprocess.call(gs_command)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def save_pdf(self, filename):
        shutil.copyfile(self.path, filename)
