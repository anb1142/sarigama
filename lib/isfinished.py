import os


def isfinished(downloadsloc, rf=False):
    artists = os.listdir(downloadsloc)
    if len(artists) < 1:
        return True
    for artist in artists:
        artistLoc = os.path.join(downloadsloc, artist)
        if not os.path.isdir(artistLoc):
            continue
        for track in os.listdir(artistLoc):
            trackLoc = os.path.join(artistLoc, track)
            if rf is True and not os.path.getsize(trackLoc):
                os.unlink(trackLoc)
