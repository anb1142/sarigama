def readData(loc):
    with open(loc) as file:
        data = file.read().splitlines()
        return data


def appendData(loc, data):
    with open(loc, 'a+') as out:
        out.write(data+"\n")
