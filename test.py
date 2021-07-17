from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import time
import requests

import os

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
options.add_argument('--window-size=1920,1080')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.headless = True
browser = webdriver.Chrome(options=options,
                           service_args=["--verbose", f"--log-path=chrome.log"])
videoUrl = 'https://mp.weixin.qq.com/s/QGW3UUfZG-XpWjC6H0Y9xQ'
audioUrl= 'https://mp.weixin.qq.com/s/JrDd6y6Bb7Z63UCGO5mg9A'
browser.get(audioUrl)
time.sleep(20)
#print(browser.execute_script('return document.body.innerHTML'))
js_tags_elem = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'js_tags'))
    )
print(js_tags_elem)
print(js_tags_elem.is_displayed())

# Show log
browserLog = browser.get_log('browser')
driverLog = browser.get_log('driver')
print(browserLog)
print(driverLog)

""" construct cookie """
mycookie = ''
cookies = browser.get_cookies()
for cookie in cookies:
    name = cookie['name']
    value = cookie['value']
    mycookie += f'{name}={value};'
print(mycookie)


#time.sleep(3)
#button = browser.find_element_by_class_name('weui-audio-btn')

button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'weui-audio-btn')))
button.click()

#time.sleep(3)
browser.save_screenshot('/home/ahei/Stories/web.png')
audioTag = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'audio')))
innerHTML = browser.execute_script("return document.body.innerHTML")
#print(innerHTML)
sel = Selector(innerHTML)

audio = sel.css('audio').xpath('@src').get()
print(audio)
print(sel.css('.weui-audio-btn'))

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
