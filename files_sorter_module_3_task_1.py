from pathlib import Path
import sys
import logging
import shutil
from threading import Thread


"""
This script sorts files from a specified folder and its subfolders by extension, 
by creating folders for each extension and copying files into them.
"""

folders_list = []


def folder_inspection(path_to_source_folder: Path) -> None:
    try:
        for item in path_to_source_folder.iterdir():
            if item.is_dir():
                folders_list.append(item)
                folder_inspection(item)
    except (FileNotFoundError, PermissionError) as error:
        logging.error(error)


def files_copying(path_to_source_folder: Path) -> None:
    try:
        for item in path_to_source_folder.iterdir():
            if item.is_file():
                extension = item.suffix[1:]
                extension_folder = destination_folder/extension
                extension_folder.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(item, extension_folder/item.name)
    except (FileNotFoundError, PermissionError) as error:
        logging.error(error)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(threadNames)s %(message)s")
    source_folder = Path(sys.argv[1])
    if len(sys.argv) < 3:
        """if a destination folder is not provided by a user, a default 'dist' folder is used"""
        destination_folder = Path("dist")
    else:
        destination_folder = Path(sys.argv[2])
    message = f"We will sort files \nfrom: {Path.absolute(source_folder)} \n  to:{Path.absolute(destination_folder)}\n"
    print(message)

    folder_inspection(source_folder)
    files_copying(source_folder)

    threads = []
    for folder in folders_list:
        th = Thread(target=files_copying, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print("Files are sorted!")
