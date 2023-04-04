import os
import sys

from func.confirmUrl import confirmUrl
from func.downloader import downloader
from func.isfinished import isfinished
from func.kickstart import kickstart
from func.manageData import appendData, readData
from func.manageFiles import md, mkfile

path = os.path.abspath(os.getcwd())
downloadsloc = os.path.join(path, '_downloads')
dataloc = os.path.join(path, '_data')

if __name__ == "__main__":
    cli = sys.argv[1:]
    if len(cli) != 0:
        if not "Unsupported" in confirmUrl(cli[0]):
            downloader(cli[0], downloadsloc, dataloc)
        elif cli[0].lower() == 'update':
            for url in readData("./_data.txt"):
                appendData('./_need.txt', url)
        guide = """Valid arguments are sarigama.lk artist links and `update`
If you haven't provided any arguments, the program will `_need.txt` for artist links"""
        sys.exit(guide)

    md([downloadsloc, dataloc])
    mkfile(['_done.txt', '_need.txt'])
    isfinished(downloadsloc, rf=True)
    kickstart(downloadsloc, dataloc)
