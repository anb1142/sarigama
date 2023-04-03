import os

def md(paths):
    paths = [paths] if isinstance(paths, list) else paths
    for path in paths:
        if not os.path.isdir(path):
            os.mkdir(path)


def mkfile(paths):
    paths = [paths] if isinstance(paths, list) else paths
    for path in paths:
        if not os.path.exists(path):
            open(path, "w").close()
