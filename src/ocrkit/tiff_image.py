import os
from wand.image import Image
from tempfile import TemporaryDirectory
import glob
import ocrkit
import pyunpaper


class TiffImage:
    def __init__(self, path: str, workfolder: TemporaryDirectory) -> None:
        self.path = path
        self.workfolder = workfolder
        self.basename = os.path.basename(self.path).split(".")[0]
        self.multipage = self.is_multipage()

    def is_multipage(self) -> bool:
        is_multipage = False
        with Image(filename=self.path, resolution=300) as img:
            if len(img.sequence) > 1:
                is_multipage = True
        return is_multipage

    def binarize_adaptive_threshold(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    page.transform_colorspace("gray")
                    page.adaptive_threshold(
                        width=16, height=16, offset=-0.08 * img.quantum_range
                    )

            img.save(filename=path_to_tiff)

        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def improve_contrast(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    numpy_page = page.numpy()
                    contrast_improved_nupmy_page = pyunpaper.improve_contrast(numpy_page)
                    contrast_improved_wand_page = Image(contrast_improved_nupmy_page)
                    page = contrast_improved_wand_page
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def deskew(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    page.deskew(0.4 * img.quantum_range)
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def multi_deskew(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    numpy_page = page.numpy()
                    deskewed_nupmy_page = pyunpaper.deskew(numpy_page)
                    deskewed_wand_page = Image(deskewed_nupmy_page)
                    page = deskewed_wand_page
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def adaptive_sharpen(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    page.adaptive_sharpen(radius=8, sigma=4)

            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def edge_detection(self, radius: float):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    page.edge(radius=radius)

            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def remove_borders(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    numpy_page = page.numpy()
                    removed_borders_nupmy_page = pyunpaper.remove_borders(numpy_page)
                    removed_borders_wand_page = Image(removed_borders_nupmy_page)
                    page = removed_borders_wand_page
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image
    
    def cropping(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    numpy_page = page.numpy()
                    cropped_nupmy_page = pyunpaper.cropping(numpy_page)
                    cropped_wand_page = Image(cropped_nupmy_page)
                    page = cropped_wand_page
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def despeckle(self): 
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    page.despeckle()
                    
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def despeckle_unpaper(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    numpy_page = page.numpy()
                    despeckled_nupmy_page = pyunpaper.despeckle(numpy_page)
                    despeckled_wand_page = Image(despeckled_nupmy_page)
                    page = despeckled_wand_page
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image   

    def remove_noise(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    numpy_page = page.numpy()
                    noise_removed_nupmy_page = pyunpaper.remove_borders(numpy_page)
                    noise_removed_wand_page = Image(noise_removed_nupmy_page)
                    page = noise_removed_wand_page
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image     
    
    def kuwahara(self):
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        with Image(filename=self.path, resolution=300) as img:
            for page_number in range(len(img.sequence)):
                with img.sequence[page_number] as page:
                    page.format = "tiff"
                    page.depth = 8
                    page.alpha_channel = "off"
                    page.kuwahara(radius=2, sigma=1.5)
                    
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image

    def save_image(self, filename):
        with Image(filename=self.path, resolution=300) as img:
            img.save(filename=filename)
    
    def rotate_image_to_corrected_text_orientation(self):
        #TODO Test if that works with multipage
        workfolder = TemporaryDirectory(dir="/RIDSS2023/tmp")
        path_to_tiff = os.path.join(workfolder.name, self.basename + ".tiff")
        pages = self.split_tiff_image()
        with Image(filename=self.path, resolution=300) as img:
            for page_number, page in enumerate(pages):
                angle = ocrkit.get_rotation_angle(page)
                with img.sequence[page_number] as img_page:
                    img_page.format = "tiff"
                    img_page.depth = 8
                    img_page.alpha_channel = "off"
                    img_page.rotate(angle)
                
            img.save(filename=path_to_tiff)
        tiff_image = TiffImage(path=path_to_tiff, workfolder=workfolder)
        return tiff_image



    def split_tiff_image(self):
        # Split preprocessed_tiff_image in seperated pages
        # TODO in Funktion
        with Image(filename=self.path) as img:
            img.save(
                filename=os.path.join(
                    self.workfolder.name, self.basename + "-page_%00000d.tif"
                )
            )
        files = glob.glob(
            os.path.join(self.workfolder.name, self.basename + "-page_*.tif")
        )

        tiff_pages = []
        for file in files:
            tiff_image = TiffImage(path=file, workfolder=self.workfolder)
            tiff_pages.append(tiff_image)
        return tiff_pages
