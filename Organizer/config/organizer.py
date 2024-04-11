import shutil
from . import settings
from pathlib import *

# Browse through every file and folder

class Organizer:

    def __init__(self, base_dir=settings.BASE_DIR, ignore_dirs=settings.IGNORE_DIRS):
        self.base_dir = Path(base_dir)
        self.ignore_dirs = ignore_dirs

    def browse_files(file_type='', is_dir=False):   

        def real_browse_files(method):
            """Browse through every file & folder before running method"""

            def wrapper(self, *args, **kwargs):
                for i in self.base_dir.glob(f'**/*{file_type}'):
                    if not any(directory in str(i.absolute()) for directory in self.ignore_dirs):
                        if is_dir == True:
                            if i.is_dir():
                                method(self, i, *args, **kwargs)
                        else: 
                            method(self, i, *args, **kwargs)
            return wrapper
        return real_browse_files

    @browse_files()
    def remove_files(self, file_object, file_types=None, file_contains=None):
        """Remove files of a specific type"""
        if file_types and file_contains:
            if file_object.suffix.lower() in file_types or file_contains in file_object.name:
                file_object.unlink()
        elif file_types or file_contains:
            if file_types:
                if file_object.suffix.lower() in file_types:
                    file_object.unlink()
            elif file_contains:
                if file_contains in file_object.stem:
                    file_object.unlink()
        else:
            raise ValueError('Remove files must at least have either file_types or file_contains argument filled in.')

    @browse_files(is_dir=True)
    def clean_folders(self, folder):
        """Remove all empty folders in directory tree"""
        if not next(folder.iterdir(), None):
            folder.rmdir()

    @browse_files()
    def copy_files(self, file_object, destination_folder_name: str, file_types: tuple):
        """Copy all files of desired file types into a desired folder"""

        destination_folder = self.base_dir / destination_folder_name
        if not destination_folder.exists():
            destination_folder.mkdir()

        # Check if file is in desired file types
        if file_object.name.lower().endswith(file_types):
            # TODO: Check if file with the same name already exists

            # Copy file into destination folder
            shutil.copy(file_object, destination_folder)

    @browse_files()
    def list_files(self, file_object, file_type=None):
        if file_type:
            if file_object.name.endswith(file_type):
                print(f'{file_object.name}')
        else:
            ftype = 'DIRECTORY' if file_object.is_dir() else 'FILE'
            print(f'{ftype}: {file_object.name}')

    @browse_files()
    def move_files(self, file_object, destination_folder_name: str, file_types: tuple):
        destination_folder = self.base_dir / destination_folder_name

        # Create destination folder if destination folder doesn't exist
        if not destination_folder.exists():
            destination_folder.mkdir()

        if file_object.suffix.lower() in file_types:
            try:
                file_object.rename(destination_folder / file_object.name)
            except:
                for i in range(10 + 1):
                    try:
                        file_object.rename(destination_folder / f'{file_object.stem} (copy {i}){file_object.suffix.lower()}')
                    except:
                        continue


        



def main():
    pass

if __name__ == '__main__':
    main()