import os,re


def isfinished(path,rf=False):
    artists = os.listdir(path)
    if len(artists) < 1:
        return True
    for artist in artists:
        artistLoc = os.path.join(path, artist)
        if not os.path.isdir(artistLoc):
            continue
        tracks = os.listdir(artistLoc)
        for track in tracks:
            trackLoc = os.path.join(artistLoc, track)

            if len(re.findall(r"mp3\.part", track)) > 0:
                if (rf == False):
                    return False
                os.unlink(trackLoc)
            elif os.path.getsize(trackLoc) == 0:
                os.unlink(trackLoc)
