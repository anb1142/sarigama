# Sarigama Downloader
#### Video Demo: https://youtu.be/xtTanvr6tbs
#### Description:
This python script downloads Sri Lankan music from Sarigama.lk when provided with artists' links. Streaming platforms don’t have lots of Sri Lankan songs. Most of the people of Sri Lanka keep their songs offline in a local library.
But when you want to download songs from an artist, it is tedious to download each song one by one. This script was made to goto the artist links of sarigama.lk and navigate to the download page and download the songs automatically.

You have to initialize it first. It creates necessary folders and text files for the user to put links.
First it checks if there’s any uncompleted downloads and deletes them.
If the argument “update” is given in the CLI, links from _done.txt file will be transferred to _needs.txt file.
Then artist links will be read from  _needs.txt file.

Duplicate elements will be removed and the urls will be  validated.
The link will then be fed to the downloader.

In earlier versions selenium was used for the downloader but later I switched to using requests for web scraping and using regular expressions to find the elements I wish to grab data from.
Using those libraries ensures compatibility, makes the program lightweight and increases performance.

The downloader then goes to the link that stores the artist's name, and gets a list of links of songs.

Songs that have already been downloaded are stored in _data and will be read using the artist’s name.

A loop iterates through a list.
The song title is stored and was acquired using regular expressions.


When iterating through that list, if the song is already downloaded according to the data we just read, it will skip that song. (The cookies are grabbed and passed to requests.)

If not skipped, the download url and save location will be passed to the download function.
It uses multiprocessing to download multiple songs at once.
Initially threading was chosen for this, due to it being unkillable, multiprocessing was chosen in its place. Luckily the change was made very early. I had to remake the script when switching to using requests and regular expressions from selenium.

How many files are downloaded at once is checked by seeing how many files are in the current artist’s folder. The script will only download 8 songs at a time.

List of each song downloaded is listed in the data folder. There is a text file for each artist and in the file, the songs are listed line by line.

Text files were chosen as the store method so that some with decent computer knowledge can access it with ease. Not making a GUI also helped to lessen the development time.

At the end if the script has iterated over every song,
the artist's link is removed from _needs.txt file and is appended to _done.txt

_needs.txt file will be read once again at the end of the script to see if the user has added any more artist links.
