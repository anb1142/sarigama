import os
from pathlib import Path

from lib.manageData import append_data, read_data


def filter_urls(urls, artist_loc, artist_data_loc):
    links = []
    artist_data = read_data(artist_data_loc)
    for url in urls:
        if (song_title := url.text.strip()) not in artist_data:
            filepath = Path(artist_loc, f'{song_title}.mp3')
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                append_data(artist_data_loc, song_title)
            else:
                links.append((url['href'], song_title, filepath))

    return links, len(urls)
