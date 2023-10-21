import os
import tkinter as tk
from tkinter import filedialog

from duplicates_remover import DuplicatesRemover
from logger import logger


def choose_directory(label_text, init_dir=None):
    directory = filedialog.askdirectory(title=label_text,
                                        initialdir=init_dir)
    return directory


def main():
    root = tk.Tk()
    root.withdraw()

    source_folder = choose_directory("Select master folder")
    target_folder = choose_directory("Select slave folder"
                                     "(where duplicates will be removed)",
                                     init_dir=os.path.dirname(source_folder))

    d = DuplicatesRemover()
    logger.info(f"Duplicates remover v{d.version}")
    result = d.delete_duplicate_files(source_folder, target_folder)
    logger.info(f"Finished! "
                f"(compared: {result.get('compared')}, "
                f"deleted: {result.get('deleted')})")


if __name__ == "__main__":
    main()
