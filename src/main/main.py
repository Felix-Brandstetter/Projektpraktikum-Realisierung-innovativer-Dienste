from wand.image import Image
import preparation
import wand


def main(file):
    file_format = preparation.get_file_format(file)
    if file_format == "PDF":
        print("Is PDF")
        if preparation.is_pdf_digital(file):
            print("PDF is digital")
            preparation.move_file_to_folder(
                file, "/RIDSS2023/outputfolder", override=True
            )
        else:
            print("Pdf is scanned")
    else:
        print("Is no PDF")
        file = preparation.convert_to_pdf(file)

    # preparation.move_file_to_folder(file,"/RIDSS2023/outputfolder",override=True)


if __name__ == "__main__":
    main("/RIDSS2023/inputfolder/icon.png")
