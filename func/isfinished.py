import os


def isfinished(downloadsloc, rf=False):
    artists = os.listdir(downloadsloc)
    if len(artists) < 1:
        return True
    for artist in artists:
        artistLoc = os.path.join(downloadsloc, artist)
        if not os.path.isdir(artistLoc):
            continue
        tracks = os.listdir(artistLoc)
        for track in tracks:
            trackLoc = os.path.join(artistLoc, track)
            if rf == True and os.path.getsize(trackLoc) == 0:
                os.unlink(trackLoc)
