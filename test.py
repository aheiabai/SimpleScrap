from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parsel import Selector
import time
import requests

import os

options = Options()
#options.headless = True
browser = webdriver.Chrome(options=options,
                           service_args=["--verbose", f"--log-path=chrome.log"])
videoUrl = 'https://mp.weixin.qq.com/s/QGW3UUfZG-XpWjC6H0Y9xQ'
audioUrl= 'https://mp.weixin.qq.com/s/JrDd6y6Bb7Z63UCGO5mg9A'
browser.get(audioUrl)

""" construct cookie """
mycookie = ''
cookies = browser.get_cookies()
for cookie in cookies:
    name = cookie['name']
    value = cookie['value']
    mycookie += f'{name}={value};'
print(mycookie)


time.sleep(3)
browser.find_element_by_class_name('weui-audio-btn').click();
innerHTML = browser.execute_script("return document.body.innerHTML")
#print(innerHTML)
sel = Selector(innerHTML)

audio = sel.css('audio').xpath('@src').get()
print(audio)

response = requests.get(audio, headers={'cookie': mycookie,'referer': audioUrl})
audioName = sel.css(".audio_card_title::text").get()
storedPath = "AudioWeb/"
if not os.path.exists(storedPath):
    os.makedirs(storedPath)

filename = f'{audioName}.mp3'
filelocation = storedPath + filename
with open(filelocation, 'wb') as f:
    f.write(response.content)
print("FINISH")


browser.quit();