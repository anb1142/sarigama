import re
from collections import OrderedDict

from .downloader import downloader
from .manageData import appendData, readData

NEED_LOC = "./_need.txt"
DONE_LOC = "./_done.txt"


def confirmUrl(url):
    url = url.replace('\n', '')
    if len(re.findall(r"sarigama\.lk\/artist\/.+\/.+", url)) < 1:
        return f"Unsupported link:\n{url}\n"

    url = "https://"+url if len(re.findall(r"(https?:\/\/)", url)) < 1 else url.replace('http://', 'https://')
    return url


def readNeeds():
    return list(OrderedDict.fromkeys((readData(NEED_LOC))))


def removeFirstLine(loc):
    with open(loc, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(loc, 'w') as fout:
        fout.writelines(data[1:])


def kickstart(downloadsloc, dataloc):
    for url in (needs := readNeeds()):
        if "Unsupported" in (url := confirmUrl(url)):
            print(url)
        elif (res := downloader(url, downloadsloc, dataloc)) == True:
            removeFirstLine(NEED_LOC)
            appendData(DONE_LOC, url)
        else:
            print(res)
    if needs != readNeeds():
        kickstart(downloadsloc, dataloc)
