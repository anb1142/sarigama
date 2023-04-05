from .downloader import downloader
from .manageData import appendData, readData


def kickstart(downloadsloc, dataloc):
    needsLoc = "./_need.txt"
    needs = []
    while needs != readData(needsLoc):
        needs = readData(needsLoc)
        for url in needs:
            if url.strip() == '':
                continue
            if (res := downloader(url, downloadsloc, dataloc)) == True:
                with open(needsLoc, 'r') as fin:
                    data = fin.read().splitlines(True)
                with open(needsLoc, 'w') as fout:
                    fout.writelines(data[1:])
                appendData('./_done.txt', url)
            else:
                print(res)
