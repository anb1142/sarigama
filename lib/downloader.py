import multiprocessing as mp
import os
import re
import time

import requests


from .manageData import appendData, readData
from .manageFiles import md


ALLOWED_CONCURRENT_DOWNLOADS = 3


def download(title, url, filepath, dataLoc, cookies):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        appendData(dataLoc, title)
        return

    try:
        fileres = requests.get(url, cookies=cookies, stream=True)
    except Exception:
        return "Request"

    with open(filepath, 'wb') as file:
        file.write(fileres.content)

    print(f"{title} has downloaded.")
    appendData(dataLoc, title)


def concurrentDownloadCounter(artistLoc):
    return len([track for track in os.listdir(artistLoc) if os.path.getsize(os.path.join(artistLoc, track)) == 0])


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

    if not (songCount := len(songurls)):
        print(f"======{artistname} ({linkCount} / {linkCount}) Songs======\n")
        return True

    print(f"======{artistname} ({songCount} Songs to Download | {linkCount-songCount} / {linkCount})======")

    artistLoc = os.path.join(downloadsloc, artistname)
    md(os.path.join(artistLoc))

    for n, (url, songtitle) in enumerate(songurls):
        downloadPageUrl = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/songs.+?)\"", requests.get(url).text)[0]
        mp3url = re.findall(r"<a.+href=\"(.+)\".+Click here to download again", requests.get(downloadPageUrl, cookies=cookies).text)[0]
        mp3loc = os.path.join(artistLoc, f'{songtitle.strip()}.mp3')

        while concurrentDownloadCounter(artistLoc)+1 >= ALLOWED_CONCURRENT_DOWNLOADS:
            time.sleep(1)

        p = mp.Process(target=download, args=(songtitle, mp3url, mp3loc, artistDlSongsLoc, cookies))
        p.start()

    if 'p' in vars():
        p.join()

    if n+1 == songCount:
        print(f"======{artistname} ({linkCount} / {linkCount}) Songs======\n")
        return True

    else:
        return "Failed to go through all songs"
