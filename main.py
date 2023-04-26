import os
import sys

from func.isfinished import isfinished
from func.kickstart import kickstart
from func.manageData import appendData, readData
from func.manageFiles import md, mkfile

PATH = os.path.abspath(os.getcwd())
DOWNLOAD_LOC = os.path.join(PATH, '_downloads')
DATA_LOC = os.path.join(PATH, '_data')

if __name__ == "__main__":
    cli = sys.argv[1:]
    if 'update' in sys.argv:
        for url in readData("./_data.txt"):
            appendData('./_need.txt', url)

    md([DOWNLOAD_LOC, DATA_LOC])
    mkfile(['_done.txt', '_need.txt'])
    isfinished(DOWNLOAD_LOC, rf=True)
    kickstart(DOWNLOAD_LOC, DATA_LOC)
