import time
from .downloader import downloader
from .manageData import appendData, readData
from .confirmUrl import confirmUrl


def kickstart(downloadsloc, dataloc):
    needsLoc = "./_need.txt"
    needs = readData(needsLoc)
    if len(needs) == 0:
        print("Instructions: To start downloading put artist links in `_need.txt`.\nEach link in a seperate line")
        time.sleep(3)
    while needs != (newNeeds := readData(needsLoc)):
        needs = list(set(newNeeds))
        for url in needs:
            url = confirmUrl(url)
            if "Unsupported" in url:
                print(url)
            if (res := downloader(url, downloadsloc, dataloc)) == True:
                with open(needsLoc, 'r') as fin:
                    data = fin.read().splitlines(True)
                with open(needsLoc, 'w') as fout:
                    fout.writelines(data[1:])
                appendData('./_done.txt', url)
            else:
                print(res)
