import multiprocessing as mp
import os
import re

import requests

from func.confirmUrl import confirmUrl

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


def downloader(url, downloadloc, dataloc):
    url = confirmUrl(url)
    if "Unsupported" in url:
        return url

    artisttext = requests.get(url).text
    artist = re.findall(r"class=\"page-title\">\n+.+<h1.+?>(.+)</h1>", artisttext)[0]

    songsurls = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/sinhala-song.+?)\"", artisttext)
    print(f"======{artist} ({len(songsurls)} Songs)======")

    artistdataLoc = os.path.join(dataloc, f'{artist}.txt')
    artistData = readData(artistdataLoc)
    
    reMsg = 0
    downCount=0
    for songurl in songsurls:
        songtext = requests.get(songurl).text
        title = re.findall(r"class=\"page-title\">\n+.+<h1.+?>(.+)</h1>", songtext)[0]
        if title in artistData:
            reMsg = 1
            print(f"{title} was already downloaded.")
            continue

        downurl = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/songs.+?)\"", songtext)[0]
        downres = requests.get(downurl, cookies=cookies)
        mp3url = re.findall(r"<a.+href=\"(.+)\".+Click here to download again", downres.text)[0]
        md(os.path.join(downloadloc, artist))
        mp3loc = os.path.join(downloadloc, artist, f'{title}.mp3')
        p = mp.Process(target=download, args=(title, mp3url, mp3loc, cookies, artistdataLoc))
        p.start()
        downCount+=1
        
    if downCount>0:
        p.join()
    if reMsg != 0:
        print("\nRemove song title from `_data` to redownload.")
    print("\n")
    
    
    return True
