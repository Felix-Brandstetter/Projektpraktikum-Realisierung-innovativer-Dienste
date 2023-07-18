import tempfile
import os
from wand.image import Image
from ocrkit.tiff_image import TiffImage
import subprocess
import shutil

## Class that defines the PDFs given as Input for OCR, and provides
## methods for converting a PDF file to a TIFF image as well as saving the PDF

class InputPDF:
    def __init__(
        self, path: str, workfolder: tempfile.TemporaryDirectory = None
    ) -> None:
        self.path = path
        self.basename = os.path.basename(self.path).split(".")[0]
        self.workfolder = workfolder

    def convert_to_tiff(self) -> TiffImage:
        # TODO: Resize to A4
        # Create a temporary working folder
        workfolder = tempfile.TemporaryDirectory()
        # Define the path to save the TIFF file
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Convert PDF to TIFF using the Wand library
        with Image(filename=self.path, resolution=300) as img:
            img.format = "tiff"  # Set the output format as TIFF
            img.depth = 8  # Set the color depth to 8 bits
            img.alpha_channel = "off"  # Disable the alpha channel (transparency)
            img.save(filename=path_to_tiff)  # Save the image as TIFF
        # Create a TiffImage object with the path and working folder
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        # Return the TiffImage object
        return tiff_image


    def convert_to_tiff_with_ghostscript(
        self,
        dpi: int = 300,
        auto_rotate_pages: bool = True,
    ):
        # Create a temporary working folder
        workfolder = tempfile.TemporaryDirectory()
        # Define the path to save the TIFF file
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Build the Ghostscript command
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
        # Insert the auto-rotate option if enabled
        if auto_rotate_pages:
            gs_command.insert(-2, "-dAutoRotatePages=/PageByPage")
        # Convert PDF to TIFF using Ghostscript command line
        subprocess.call(gs_command)
        # Create a TiffImage object with the path and working folder
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        # Return the TiffImage object
        return tiff_image

    def convert_to_tiff_with_imagemagick(
        self,
        dpi: int = 300,
        auto_rotate_pages: bool = True,
        width: int = 0,
        height: int = 0
    ):
        # Create a temporary working folder
        workfolder = tempfile.TemporaryDirectory()
        # Define the path to save the TIFF file
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        # Build the ImageMagick command
        magick_command = [
            "magick",
            "-density",
            "{}".format(dpi),
            self.path,
            "-compress",
            "LZW",
            self.path
        ]
        # Append the auto-rotate option if enabled
        if auto_rotate_pages:
            magick_command.append("-auto-rotate")
        # Append the resize option if width and height are specified
        if width != 0 and height != 0:
            magick_command.extend(["-resize", "{}x{}>".format(width, height)])
        # Append the path to save the TIFF file
        magick_command.append(path_to_tiff)
        # Convert PDF to TIFF using ImageMagick command line
        subprocess.call(magick_command)
        # Create a TiffImage object with the path and working folder
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        # Return the TiffImage object
        return tiff_image

    def save_pdf(self, filename):
        # Save the PDF file to a new location with the given filename
        shutil.copyfile(self.path, filename)
