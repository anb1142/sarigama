import multiprocessing as mp
import os
import re
import time

import requests


from .manageData import appendData, readData
from .manageFiles import md

session = requests.Session()
session.get('https://sarigama.lk')
cookies = session.cookies.get_dict()


def download(title, url, filepath, cookies, dataLoc):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        appendData(dataLoc, title)
        print(f"{title} was already downloaded.")
    try:
        fileres = requests.get(url, cookies=cookies, stream=True)
    except:
        return "Request"

    with open(filepath, 'wb') as file:
        file.write(fileres.content)

    print(f"{title} has downloaded.")
    appendData(dataLoc, title)


def downloadingCount(artistLoc):
    i = 0
    for track in os.listdir(artistLoc):
        if os.path.getsize(os.path.join(artistLoc, track)) == 0:
            i += 1
    return i


def downloader(url, downloadsloc, dataloc):
    artisttext = requests.get(url).text
    artist = re.findall(r"class=\"page-title\">\n+.+<h1.+?>(.+)</h1>", artisttext)[0]

    songsurls = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/sinhala-song.+?)\"", artisttext)
    print(f"======{artist} ({len(songsurls)} Songs)======")

    artistdataLoc = os.path.join(dataloc, f'{artist}.txt')
    artistData = readData(artistdataLoc)

    n=0
    reMsg = 0
    downCount = 0
    for songurl in songsurls:
        n+=1
        songtext = requests.get(songurl).text
        title = re.findall(r"class=\"page-title\">\n+.+<h1.+?>(.+)</h1>", songtext)[0]
        if title in artistData:
            reMsg = 1
            print(f"{title} was already downloaded.")
            continue

        downurl = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/songs.+?)\"", songtext)[0]
        downres = requests.get(downurl, cookies=cookies)
        mp3url = re.findall(r"<a.+href=\"(.+)\".+Click here to download again", downres.text)[0]

        artistLoc = os.path.join(downloadsloc, artist)
        md(os.path.join(artistLoc))
        mp3loc = os.path.join(artistLoc, f'{title}.mp3')

        currentCount = downloadingCount(artistLoc)
        while currentCount > 7:
            currentCount = downloadingCount(artistLoc)
            time.sleep(1)
        p = mp.Process(target=download, args=(title, mp3url, mp3loc, cookies, artistdataLoc))
        p.start()
        downCount += 1
        
    if downCount > 0:
        p.join()
    if reMsg != 0:
        print("\nRemove song title from `_data` to redownload.")
    print("\n")

    if n == len(songsurls):
        return True
    return "Failed to go through all songs"
