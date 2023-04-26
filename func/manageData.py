import os


def readData(path):
    if not os.path.exists(path):
        return []
    with open(path) as file:
        return file.read().splitlines()


def appendData(path, data):
    with open(path, 'a+') as out:
        out.write(data.strip()+"\n")
