import time
from collections import OrderedDict
from .downloader import downloader
from .manageData import appendData, readData
from .confirmUrl import confirmUrl


def kickstart(downloadsloc, dataloc):
    needsLoc = "./_need.txt"
    needs = []
    if len((newNeeds := readData(needsLoc))) == 0:
        print("Instructions: To start downloading put artist links in `_need.txt`.\nEach link in a seperate line")
        time.sleep(3)
    while needs != (newNeeds := readData(needsLoc)):
        needs = list(OrderedDict.fromkeys(newNeeds))
        for url in needs:
            url = confirmUrl(url)
            if "Unsupported" in url:
                print(url)
                continue
            if (res := downloader(url, downloadsloc, dataloc)) == True:
                with open(needsLoc, 'r') as fin:
                    data = fin.read().splitlines(True)
                with open(needsLoc, 'w') as fout:
                    fout.writelines(data[1:])
                appendData('./_done.txt', url)
            else:
                print(res)
