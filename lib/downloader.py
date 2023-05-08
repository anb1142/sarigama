import multiprocessing as mp
import os
import re
import time
from pathlib import Path

import requests

from ._vars import DATA_LOC, DOWNLOAD_LOC
from .manageData import append_data, read_data
from .manageFiles import md

ALLOWED_CONCURRENT_DOWNLOADS = 3


def download(title, url, filepath, artist_data_loc, cookies):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        append_data(artist_data_loc, title)
        return

    try:
        fileres = requests.get(url, cookies=cookies, stream=True)
    except Exception:
        return "Request"

    with open(filepath, 'wb') as file:
        file.write(fileres.content)

    print(f"{title} has downloaded.")
    append_data(artist_data_loc, title)


def concurrentDownloadCounter(artistLoc):
    return len([track for track in os.listdir(artistLoc) if os.path.getsize(Path(artistLoc, track)) == 0])


def downloader(url):
    session = requests.Session()
    session.get('https://sarigama.lk')
    cookies = session.cookies.get_dict()

    artist_page_html = requests.get(url).text

    artistname = re.findall(r"class=\"page-title\">\n+.+<h1.+?>(.+)</h1>", artist_page_html)[0]
    songurls = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/sinhala-song.+?)\">\n?(.+?)<\/a>", artist_page_html)
    link_count = len(songurls)

    artist_data_loc = Path(DATA_LOC, f'{artistname}.txt')
    songurls = [song for song in songurls if song[1].strip() not in read_data(artist_data_loc)]

    if not (song_count := len(songurls)):
        print(f"======{artistname} ({link_count} / {link_count}) Songs======\n")
        return True

    print(f"======{artistname} ({song_count} Songs to Download | {link_count-song_count} / {link_count})======")

    artist_loc = Path(DOWNLOAD_LOC, artistname)
    md(Path(artist_loc))

    for n, (url, songtitle) in enumerate(songurls):
        download_page_url = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/songs.+?)\"", requests.get(url).text)[0]
        mp3url = re.findall(r"<a.+href=\"(.+)\".+Click here to download again", requests.get(download_page_url, cookies=cookies).text)[0]
        mp3loc = Path(artist_loc, f'{songtitle.strip()}.mp3')

        while concurrentDownloadCounter(artist_loc)+1 >= ALLOWED_CONCURRENT_DOWNLOADS:
            time.sleep(1)

        p = mp.Process(target=download, args=(songtitle, mp3url, mp3loc, artist_data_loc, cookies))
        p.start()

    if 'p' in vars():
        p.join()

    if n+1 == song_count:
        print(f"======{artistname} ({link_count} / {link_count}) Songs======\n")
        return True

    else:
        return "Failed to go through all songs"
