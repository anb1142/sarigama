import os

from func.manageFiles import md, mkfile
from func.isfinished import isfinished
from func.kickstart import kickstart

path = os.path.join(os.path.abspath(os.getcwd()), '_downloads')


def main():
    md(path)
    mkfile(['_done.txt', '_need.txt'])
    isfinished(True)
    kickstart()
    


if __name__ == "__main__":
    main()
