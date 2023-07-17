import music_tag


def add_meta_tags(filepath, title, album, artwork):
    # TODO con_artists
    # TODO if art not exist
    song = music_tag.load_file(filepath)
    for rem in ['title', 'album', 'artist', 'artwork']:
        song.remove_tag(rem)

    with open(artwork, 'rb') as img_in:
        song['artwork'] = img_in.read()

    song['title'] = title
    song['album'] = album
    song['genre'] = "Sri Lankan"

    song.save()
