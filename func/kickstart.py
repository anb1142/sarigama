from .downloader import downloader
from .manageData import appendData, readData




def kickstart(path):
    needsLoc = "./_need.txt"
    needs = []

    if len(needs)==0:
        print("No URLs provided")
        return 
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
