import os
from pathlib import Path

from ._vars import DOWNLOAD_LOC


def isfinished(rf=False):
    artists = os.listdir(DOWNLOAD_LOC)
    if not len(artists):
        return True
    for artist in artists:
        artist_loc = Path(DOWNLOAD_LOC, artist)
        if not os.path.isdir(artist_loc):
            continue
        for track in os.listdir(artist_loc):
            track_loc = Path(artist_loc, track)
            if rf is True and not os.path.getsize(track_loc):
                os.unlink(track_loc)
