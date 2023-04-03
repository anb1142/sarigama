from downloader import downloader
from manageData import appendData, readData

from ..main import path


def kickstart():
    needsLoc = "./_need.txt"
    needs = []

    print("Downloading Started")
    while needs != readData(needsLoc):
        needs = readData(needsLoc)
        for url in needs:
            if downloader(url, path) == True:
                with open(needsLoc, 'r') as fin:
                    data = fin.read().splitlines(True)
                with open(needsLoc, 'w') as fout:
                    fout.writelines(data[1:])
                appendData('./_done.txt', url)
    print("Downloading Finished")
