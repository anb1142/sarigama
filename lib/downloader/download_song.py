
import requests
from bs4 import BeautifulSoup as bs4

from lib._vars import PARSER
from lib.downloader.add_meta_tags import add_meta_tags
from lib.downloader.download_file import download_file
from lib.manageData import append_data


def download_song(data, artist_name,  artist_data_loc, artwork_url, cookies):
    song_url, song_title, filepath = data
    song_page = bs4(requests.get(song_url).content, PARSER)

    con_artists = song_page.find("table", {"class": "contributers"}).findAll("span", {"itemprop": "byArtist"})
    con_artists = artist_name if len(con_artists) < 2 else ", ".join([elem.text for elem in con_artists])

    try:
        download_page_url = song_page.find("a", {"class": "btn btn-primary btn-lg btn-fix-size", "target": "_blank"})['href']
    except TypeError:
        append_data(artist_data_loc, song_title)
        return

    download_page = bs4(requests.get(download_page_url, cookies=cookies).content, PARSER)
    mp3url = download_page.find(id="block_204").parent.find("a")['href']

    if download_file(mp3url, filepath, cookies):
        add_meta_tags(filepath, song_title, artist_name, artwork_url)
        print(f"{song_title} has been downloaded.")
        append_data(artist_data_loc, song_title)
    else:
        print(f"Failed to download {song_title}.")
