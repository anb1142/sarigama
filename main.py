import os
import sys

from func.isfinished import isfinished
from func.kickstart import kickstart
from func.manageData import appendData, readData
from func.manageFiles import md, mkfile

path = os.path.abspath(os.getcwd())
downloadsloc = os.path.join(path, '_downloads')
dataloc = os.path.join(path, '_data')

if __name__ == "__main__":
    cli = sys.argv[1:]
    if 'update' in sys.argv:
        for url in readData("./_data.txt"):
            appendData('./_need.txt', url)

    md([downloadsloc, dataloc])
    mkfile(['_done.txt', '_need.txt'])
    isfinished(downloadsloc, rf=True)
    kickstart(downloadsloc, dataloc)
