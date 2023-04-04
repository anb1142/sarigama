import re


def confirmUrl(url):
    url=url.replace('\n', '')
    if len(re.findall(r"sarigama\.lk\/artist\/.+\/.+", url)) < 1:
        return f"Unsupported link:\n{url}\n"

    url = "https://"+url if len(re.findall(r"(https?:\/\/)", url)) < 1 else url.replace('http://', 'https://')
    return url
