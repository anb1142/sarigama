import re


def find_artwork__url(artist_page):
    art_elem = artist_page.find("div", {"class": "padding b-b"}).find('div', 'item-media-content')['style']
    url = re.findall(r"url\('?(.+?)'?\)", art_elem)[0]
    if 'default' in url:
        return None
    return url
