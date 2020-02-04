import dotenv
import os
import pathlib
import random

dotenv.load_dotenv()


class GutenbergFiles:

    def __init__(self, directory=None, file_extension='zip'):
        if directory is None:
            directory = os.environ.get('GUTENBERG_DIR')
        self.directory = directory
        self.files = None
        self.file_extension = file_extension

    def _get_files(self):
        if self.files is None:
            if self.directory is None:
                self.files = []
            else:
                dir_path = pathlib.Path(self.directory).absolute()
                self.files = list(dir_path.rglob(
                    '*.{}'.format(self.file_extension)))
                # TODO: Is this appropriate:
                self.files = [book_path for book_path in self.files
                              if '-' not in book_path.name]
        return self.files

    def get_files(self, order='glob'):
        order = order.strip().lower()
        if order == 'lexicographical':
            book_paths = sorted(self._get_files(), key=lambda bp: bp.name)
        elif order == 'numerical':
            book_paths = sorted(self._get_files(),
                                key=lambda bp: int(bp.name.rstrip(
                                    '.{}'.format(self.file_extension))))
        elif order == 'random':
            book_paths = random.sample(self._get_files(),
                                       k=len(self._get_files()))
        else:
            book_paths = self._get_files()
        yield from book_paths

# numbers = [int(b.name.rstrip('.zip').split('-')[0]) for b in books]
# un_dash_numbers = [int(b.name.rstrip('.zip')) for b in books
#                    if '-' not in b.name]
