import os
import sys

from lib.isfinished import isfinished
from lib.kickstart import kickstart
from lib.manageData import appendData, readData
from lib.manageFiles import md, mkfile

PATH = os.path.abspath(os.getcwd())
DOWNLOAD_LOC = os.path.join(PATH, '_downloads')
DATA_LOC = os.path.join(PATH, '_data')
DONE_LOC = './_done.txt'

if __name__ == "__main__":
    md([DOWNLOAD_LOC, DATA_LOC])
    mkfile(['_done.txt', '_need.txt'])
    isfinished(DOWNLOAD_LOC, rf=True)
    cli = sys.argv[1:]
    if 'update' in sys.argv:
        for url in readData(DONE_LOC):
            appendData('./_need.txt', url)
        os.unlink(DONE_LOC)
        mkfile(DONE_LOC)
    kickstart(DOWNLOAD_LOC, DATA_LOC)
