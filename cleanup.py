import os
import shutil


class PyCacheCleaner:
    def __init__(self, dir_path="."):
        self.dir_path = dir_path

    def remove_pycache(self):
        """
        Removes all __pycache__ folders in the specified directory and its subdirectories.
        """
        for root, dirs, files in os.walk(self.dir_path, topdown=False):
            for name in dirs:
                if name == "__pycache__":
                    try:
                        full_path = os.path.join(root, name)
                        shutil.rmtree(full_path)
                        print(f"Removed: {full_path}")
                    except Exception as e:
                        print(f"Error removing {full_path}: {e}")


if __name__ == "__main__":
    cleaner = PyCacheCleaner(".")
    cleaner.remove_pycache()
