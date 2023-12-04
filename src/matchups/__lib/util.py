import os

class HelperUtil:

    def __init__(self):
        pass

    def get_all_filepaths_by_extension(self, path_to_dir, extension) -> list:
        _filePaths = []

        for _dirpath, _dirnames, _filenames in os.walk(path_to_dir):
            for _filename in _filenames:
                if _filename.endswith(extension) and not _filename.startswith('.'):
                    _filePaths.append(os.path.join(_dirpath, _filename))
        return _filePaths

    def get_prefix_columns(self, prefix, start=0, end=0, step=0):
        return [f"{prefix}{number}" for number in range(start, end, step)]