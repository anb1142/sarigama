import os

import requests


def download_file(url, filepath, cookies={}, by_chunk=False):
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        headers = {'Range': f'bytes={file_size}-'}
        file_mode = 'ab'  # Append mode
    else:
        headers = {}
        file_mode = 'wb'  # Write from the beginning

    response = requests.get(url, headers=headers, cookies=cookies, stream=True)
    if response.status_code == 200 or response.status_code == 206:
        with open(filepath, file_mode) as file:
            if by_chunk:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            else:
                file.write(response.content)
        return True

    return False
