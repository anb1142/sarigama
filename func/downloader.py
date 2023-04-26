import multiprocessing as mp
import os
import re
import time

import requests


from .manageData import appendData, readData
from .manageFiles import md


ALLOWED_CONCURRENT_DOWNLOADS = 2


def download(title, url, filepath, dataLoc, cookies):
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
    session = requests.Session()
    session.get('https://sarigama.lk')
    cookies = session.cookies.get_dict()

    artistPageHtml = requests.get(url).text

    artistname = re.findall(r"class=\"page-title\">\n+.+<h1.+?>(.+)</h1>", artistPageHtml)[0]
    songurls = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/sinhala-song.+?)\">\n?(.+?)<\/a>", artistPageHtml)
    linkCount = len(songurls)

    artistDlSongsLoc = os.path.join(dataloc, f'{artistname}.txt')
    songurls = [song for song in songurls if song[1].strip() not in readData(artistDlSongsLoc)]

    if (songCount := len(songurls)) == 0:
        return True

    print(f"======{artistname} ({songCount} Songs to Download | {linkCount-songCount} / {linkCount})======")

    artistLoc = os.path.join(downloadsloc, artistname)
    md(os.path.join(artistLoc))

    for n, (url, songtitle) in enumerate(songurls):
        while downloadingCount(artistLoc)+1 >= ALLOWED_CONCURRENT_DOWNLOADS:
            time.sleep(1)

        downloadPageUrl = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/songs.+?)\"", requests.get(url).text)[0]
        mp3url = re.findall(r"<a.+href=\"(.+)\".+Click here to download again", requests.get(downloadPageUrl, cookies=cookies).text)[0]
        mp3loc = os.path.join(artistLoc, f'{songtitle}.mp3')

        p = mp.Process(target=download, args=(songtitle, mp3url, mp3loc, artistDlSongsLoc, cookies))
        p.start()

    if 'p' in vars():
        p.join()
    print("\n")

    if n+1 == songCount:
        return True
    else:
        return "Failed to go through all songs"
