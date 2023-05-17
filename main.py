import os
import sys

from lib._vars import DATA_LOC, DONE_LOC, DOWNLOAD_LOC, NEED_LOC
from lib.isfinished import isfinished
from lib.kickstart import kickstart
from lib.manageData import append_data, read_data
from lib.manageFiles import md, mkfile


def main():
    md([DOWNLOAD_LOC, DATA_LOC])
    mkfile([DONE_LOC, NEED_LOC])
    isfinished(rf=True)
    if 'update' in sys.argv:
        for url in read_data(DONE_LOC):
            append_data(NEED_LOC, url)
        os.unlink(DONE_LOC)
        mkfile(DONE_LOC)
    kickstart()


if __name__ == "__main__":
    main()
