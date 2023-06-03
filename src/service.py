import inotify.adapters
from multiprocessing import Pool, cpu_count
import os
from ocrkit_with_ocrmypdf import process_file_with_ocrmypdf
from ocrkit import process_file_with_ocrkit
#TODO Imports anpassen



def watch_inputfolder(inputfolder):
    i = inotify.adapters.Inotify()
    i.add_watch(inputfolder)
    
    while True:
        files = []
        for event in i.event_gen(yield_nones=False, timeout_s=1):
            if "IN_MOVED_TO" in event[1] or "IN_CLOSE_WRITE" in event[1]:
                file = os.path.join(event[2],event[3])
                files.append(file)

        if len(files) > 0:
            with Pool(cpu_count()-1) as pool:
                #pool.map(process_file_with_ocrmypdf, files)
                pool.map(process_file_with_ocrkit, files)



if __name__ == "__main__":
    watch_inputfolder("/RIDSS2023/inputfolder")

    


