import re
from collections import OrderedDict

from ._vars import DATA_LOC, DONE_LOC, DOWNLOAD_LOC
from .downloader import downloader
from .manageData import append_data, read_data

NEED_LOC = "./_need.txt"
DONE_LOC = "./_done.txt"


def confirm_url(url):
    url = url.replace('\n', '')
    if len(re.findall(r"sarigama\.lk\/artist\/.+\/.+", url)) < 1:
        return f"Unsupported link:\n{url}\n"

    url = "https://"+url if len(re.findall(r"(https?:\/\/)", url)) < 1 else url.replace('http://', 'https://')
    return url


def read_needs():
    return list(OrderedDict.fromkeys((read_data(NEED_LOC))))


def remove_first_line(loc):
    with open(loc, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(loc, 'w') as fout:
        fout.writelines(data[1:])


def kickstart():
    for url in (needs := read_needs()):
        if "Unsupported" in (url := confirm_url(url)):
            print(url)
        elif (res := downloader(url)) is True:
            remove_first_line(NEED_LOC)
            append_data(DONE_LOC, url)
        else:
            print(res)
    if needs != read_needs():
        kickstart(DOWNLOAD_LOC, DATA_LOC)
