import shutil
import os
import preparation


def main(file):
    file_format = preparation.get_file_format(file)
    if file_format == "PDF":
        preparation.

    #preparation.copy_file_to_folder(file,"/RIDSS2023/outputfolder",override=True)



if __name__ == "__main__":
    main("/RIDSS2023/inputfolder/Testnotenauszug.pdf")