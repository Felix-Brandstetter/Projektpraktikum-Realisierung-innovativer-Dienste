import inotify.adapters
from multiprocessing import Pool, cpu_count
import os
from ocrkit_with_ocrmypdf import process_file_with_ocrmypdf
from ocrkit import process_file_with_ocrkit
from concurrent.futures import ProcessPoolExecutor
import time

def watch_folder(folder):
    with ProcessPoolExecutor(4) as ex:
        futures = []

        file_found = True
        while file_found:
            futures = list(filter(lambda f: (f.done() is not True), futures))
            print(futures)
            if len(futures) < 4:
                file = os.listdir(folder)
                file_found = file is not None

                if file is not None:
                    future = ex.submit(process_file_with_ocrmypdf, file)
                    futures.append(future)
                else:
                    print(f"Found next queue item: False")

            time.sleep(0.5)



if __name__ == "__main__":
    watch_folder("/RIDSS2023/inputfolder")
