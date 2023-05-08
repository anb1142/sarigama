import multiprocessing as mp
import os
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from ._vars import ALLOWED_CONCURRENT_DOWNLOADS, DATA_LOC, DOWNLOAD_LOC, PARSER
from .manageData import append_data, read_data
from .manageFiles import md


def append_song_data(title):
    append_data(artist_data_loc, title)


def download(title, url, filepath):
    try:
        fileres = requests.get(url, cookies=cookies, stream=True)
    except Exception:
        print("Failed request")

    with open(filepath, 'wb') as file:
        file.write(fileres.content)

    print(f"{title} has downloaded.")
    append_song_data(title)


def concurrentDownloadCounter(artistLoc):
    return len([track for track in os.listdir(artistLoc) if os.path.getsize(Path(artistLoc, track)) < 0])


ARTIST_LINK_PREFIX = 'https://sarigama.lk/sinhala-song/'


def filter_urls(urls, artist_loc):
    links = []
    for a in urls:
        IS_NOT_IN_DATA = (song_title := a.text.strip()) not in read_data(artist_data_loc)
        filepath = Path(artist_loc, f'{song_title}.mp3')
        SONG_FILE_EXISTS = os.path.exists(filepath) and os.path.getsize(filepath) > 0

        if IS_NOT_IN_DATA:
            if SONG_FILE_EXISTS:
                append_song_data(song_title)
            else:
                links.append((a['href'], song_title, filepath))

    return links, len(urls)


artist_data_loc = ''
cookies = {}


def downloader(artist_url):
    global artist_data_loc, cookies

    session = requests.Session()
    session.get('https://sarigama.lk')
    cookies = session.cookies.get_dict()

    artist_page = BeautifulSoup(requests.get(artist_url).content, PARSER)
    artist_name = artist_page.find("h1", {"class": "inline"}).text
    artist_data_loc = Path(DATA_LOC, f'{artist_name}.txt')

    md((artist_loc := Path(DOWNLOAD_LOC, artist_name)))
    song_urls, total_songs = filter_urls(artist_page.find(id="tracks").find_all("a", {"target": "_blank"}), artist_loc)

    total_songs = len(song_urls)

    if (to_download_count := len(song_urls)) == 0:
        print(f"======{artist_name} ({total_songs} / {total_songs}) Songs======\n")
        return True

    print(f"======{artist_name} ({to_download_count} Songs to Download | {total_songs-to_download_count} / {total_songs})======")

    for n, (song_url, song_title, filepath) in enumerate(song_urls):
        artist_page = BeautifulSoup(requests.get(song_url).content, PARSER)
        try:
            download_page_url = artist_page.find("a", {"class": "btn btn-primary btn-lg btn-fix-size", "target": "_blank"})['href']
        except TypeError:
            append_song_data(song_title)
            continue

        download_page = BeautifulSoup(requests.get(download_page_url, cookies=cookies).content, PARSER)
        mp3url = download_page.find(id="block_204").parent.find("a")['href']

        while concurrentDownloadCounter(artist_loc)+1 > ALLOWED_CONCURRENT_DOWNLOADS:
            time.sleep(1)

        p = mp.Process(target=download, args=(song_title, mp3url, filepath))
        p.start()

    if 'p' in vars():
        p.join()

    if n+1 == to_download_count:
        print(f"======{artist_name} ({total_songs} / {total_songs}) Songs======\n")
        return True

    else:
        return "Failed to go through all songs"
