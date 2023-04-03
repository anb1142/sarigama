import os
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .isfinished import isfinished
from .manageData import appendData, readData

#TODO if mp3 exists

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")

def downloader(url,path):
    aritstMatch = re.findall(r"artist/(.+)/", url)
    if (len(re.findall(r"artist/(.+)/", url)) < 1):
        raise Exception("Incorrect Url: can't find \"artist/\"")
    artist = aritstMatch[0]

    artistLoc = os.path.join(path,  artist)
    dataLoc = os.path.join(os.path.join(os.path.abspath(os.getcwd()), '#data')+f'{artist}.txt')
    options.set_preference("browser.download.dir", artistLoc)

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(15)

    data = readData(dataLoc) if os.path.exists(dataLoc) else []

    print("\n==="+artist+"===\n")
    req = requests.get(url)
    for songurl in re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/sinhala-song.+?)\"", req.text):
        songreq = requests.get(songurl)

        downurl = re.findall(r"<a target=\"_blank\" href=\"(https:\/\/sarigama.lk\/songs.+?)\"", songreq.text)[0]
    print(downurl)
    return
    try:
        driver.get(url)
        tracks = driver.find_elements(By.CSS_SELECTOR, "#tracks > div")
    except:
        return "Failed to Launch"

    for trackelem in tracks:
        try:
            driver.switch_to.window(driver.window_handles[0])  # IMPORTANT must be first
            trackname = trackelem.text.strip()
            print(trackname, end=' ', flush=True)

            if trackname in data:
                print('exists', end='\n', flush=True)
                continue
            track = trackelem.find_element(By.XPATH, './/a')

            driver.execute_script("window.open('" + track.get_attribute('href') + "');")
            driver.switch_to.window(driver.window_handles[1])

            time.sleep(10)
            try:
                download = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
            except:
                appendData(dataLoc, trackname)
                driver.execute_script("window.close();")
                print('not found', end='\n', flush=True)
                continue

            download.click()

            driver.execute_script("window.close();")
            time.sleep(15)
            driver.switch_to.window(driver.window_handles[1])
            driver.execute_script("window.close();")

            fin = isfinished()
            while fin == False:
                fin = isfinished()
                time.sleep(1)

            appendData(dataLoc, trackname)
            print('done', end='\n', flush=True)
        except:
            print('failed', end='\n', flush=True)

    driver.quit()
    return True
