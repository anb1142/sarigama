import os
from pathlib import Path

PATH = os.path.abspath(os.getcwd())
DOWNLOAD_LOC = Path(PATH, '_downloads')
DATA_LOC = Path(PATH, '_data')
DONE_LOC = Path(PATH, '_done.txt')
NEED_LOC = Path(PATH, '_need.txt')

PARSER = 'html.parser'
ALLOWED_CONCURRENT_DOWNLOADS = 3
