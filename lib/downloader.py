import multiprocessing as mp
import os
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from ._vars import ALLOWED_CONCURRENT_DOWNLOADS, DATA_LOC, DOWNLOAD_LOC, PARSER
from .manageData import append_data, read_data
from .manageFiles import md


<<<<<<< HEAD
def download(song_title, url, cookies, filepath, artist_data_loc):
=======
def append_song_data(title):
    append_data(artist_data_loc, title)


def download(title, url, filepath):
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2
    try:
        fileres = requests.get(url, cookies=cookies, stream=True)
    except Exception:
        print("Failed request")

    with open(filepath, 'wb') as file:
        file.write(fileres.content)

<<<<<<< HEAD
    print(f"{song_title} has downloaded.")
    append_data(artist_data_loc, song_title)


def concurrentDownloadCounter(artist_loc):
    return len([track for track in os.listdir(artist_loc) if os.path.getsize(Path(artist_loc, track)) == 0])
=======
    print(f"{title} has downloaded.")
    append_song_data(title)


def concurrentDownloadCounter(artistLoc):
    return len([track for track in os.listdir(artistLoc) if os.path.getsize(Path(artistLoc, track)) < 0])
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2


ARTIST_LINK_PREFIX = 'https://sarigama.lk/sinhala-song/'


<<<<<<< HEAD
def filter_urls(urls, artist_loc, artist_data_loc):
=======
def filter_urls(urls, artist_loc):
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2
    links = []
    for a in urls:
        IS_NOT_IN_DATA = (song_title := a.text.strip()) not in read_data(artist_data_loc)
        filepath = Path(artist_loc, f'{song_title}.mp3')
        SONG_FILE_EXISTS = os.path.exists(filepath) and os.path.getsize(filepath) > 0

        if IS_NOT_IN_DATA:
            if SONG_FILE_EXISTS:
<<<<<<< HEAD
                append_data(artist_data_loc, song_title)
=======
                append_song_data(song_title)
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2
            else:
                links.append((a['href'], song_title, filepath))

    return links, len(urls)


<<<<<<< HEAD
def downloader(artist_url):
=======
artist_data_loc = ''
cookies = {}


def downloader(artist_url):
    global artist_data_loc, cookies

>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2
    session = requests.Session()
    session.get('https://sarigama.lk')
    cookies = session.cookies.get_dict()

    artist_page = BeautifulSoup(requests.get(artist_url).content, PARSER)
    artist_name = artist_page.find("h1", {"class": "inline"}).text
    artist_data_loc = Path(DATA_LOC, f'{artist_name}.txt')

    md((artist_loc := Path(DOWNLOAD_LOC, artist_name)))
<<<<<<< HEAD
    song_urls, total_songs = filter_urls(artist_page.find(id="tracks").find_all("a", {"target": "_blank"}), artist_loc, artist_data_loc)
=======
    song_urls, total_songs = filter_urls(artist_page.find(id="tracks").find_all("a", {"target": "_blank"}), artist_loc)
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2

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
<<<<<<< HEAD
            append_data(artist_data_loc, song_title)
=======
            append_song_data(song_title)
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2
            continue

        download_page = BeautifulSoup(requests.get(download_page_url, cookies=cookies).content, PARSER)
        mp3url = download_page.find(id="block_204").parent.find("a")['href']
<<<<<<< HEAD
        while concurrentDownloadCounter(artist_loc)+1 > ALLOWED_CONCURRENT_DOWNLOADS:
            time.sleep(1)
        p = mp.Process(target=download, args=(song_title, mp3url, cookies, filepath, artist_data_loc))
=======

        while concurrentDownloadCounter(artist_loc)+1 > ALLOWED_CONCURRENT_DOWNLOADS:
            time.sleep(1)

        p = mp.Process(target=download, args=(song_title, mp3url, filepath))
>>>>>>> bfc44e7b6eb6dc7ad97c10045415422bc91dd4c2
        p.start()

    if 'p' in vars():
        p.join()

    if n+1 == to_download_count:
        print(f"======{artist_name} ({total_songs} / {total_songs}) Songs======\n")
        return True

    else:
        return "Failed to go through all songs"
