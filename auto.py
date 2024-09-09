import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DIRECTORY = os.path.join(os.path.expanduser("D:\\"), "Downloads")
EXTENSIONS = {
    ".txt": "Text File",
    ".pdf": "Document",
    ".doc": "Document",
    ".docx": "Document",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".mp3": "Music",
    ".wav": "Music",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".zip": "ZIP Archive",
    ".exe": "Softwares",
    ".pptx": "PPTs",
    ".ttf": "Fonts",
}


class MovingFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            self.move_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            time.sleep(1)
            self.move_file(event.src_path)

    def move_file(self, file_path):
        if os.path.isfile(file_path):
            extension = os.path.splitext(file_path)[1].lower()

            if extension in EXTENSIONS:
                folder_name = EXTENSIONS[extension]
                folder_path = os.path.join(DIRECTORY, folder_name)
                os.makedirs(folder_path, exist_ok=True)

                destination_path = os.path.join(
                    folder_path, os.path.basename(file_path)
                )

                if not os.path.exists(destination_path):
                    shutil.move(file_path, destination_path)
                    print(
                        f"Moved {os.path.basename(file_path)} to {folder_name} folder"
                    )
                else:
                    print(
                        f"Skipped {os.path.basename(file_path)}. File already exists in destination."
                    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    event_handler = MovingFileHandler()
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
