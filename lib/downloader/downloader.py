import multiprocessing as mp
from pathlib import Path

import requests
from bs4 import BeautifulSoup as bs4

from lib.downloader.download_song import download_song
from lib.downloader.filter_urls import filter_urls
from lib.downloader.find_artist_image_url import find_artwork__url

from .._vars import (ALLOWED_CONCURRENT_DOWNLOADS, DATA_LOC, DOWNLOAD_LOC,
                     PARSER)
from ..manageFiles import md

session = requests.Session()
session.get('https://sarigama.lk')
cookies = session.cookies.get_dict()


def downloader(artist_url):
    artist_page = bs4(requests.get(artist_url).content, PARSER)

    artist_name = artist_page.find("h1", {"class": "inline"}).text
    artist_data_loc = Path(DATA_LOC, f'{artist_name}.txt')
    artwork_url = find_artwork__url(artist_page)

    md((artist_loc := Path(DOWNLOAD_LOC, artist_name)))
    song_urls, total_songs = filter_urls(artist_page.find(id="tracks").find_all("a", {"target": "_blank"}), artist_loc, artist_data_loc)

    total_songs = len(song_urls)

    if (to_download_count := len(song_urls)) == 0:
        print(f"======{artist_name} ({total_songs} / {total_songs}) Songs======\n")
        return True

    print(f"======{artist_name} ({to_download_count} Songs to Download | {total_songs-to_download_count} / {total_songs})======")

    pool = mp.Pool(ALLOWED_CONCURRENT_DOWNLOADS)
    for n, data in enumerate(song_urls):
        pool.apply_async(download_song, args=(data, artist_name,  artist_data_loc, artwork_url, cookies))

    pool.close()
    pool.join()

    if n+1 == to_download_count:
        print(f"======{artist_name} ({total_songs} / {total_songs}) Songs======\n")
        return True

    else:
        return "Failed to go through all songs"
