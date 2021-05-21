from pyppeteer import launch
import asyncio
import time
import requests
import os
import threading
import logging

async def main(url):
    logging.warning(threading.current_thread().name)
    
    audioUrl = url
    # start browser and disable signal
    browser = await launch(headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
    # 创建一个页面
    page = await browser.newPage()
   
    await page.goto(audioUrl)
    """ construct cookie """
    mycookie = ''
    cookies = await page.cookies()
    for cookie in cookies:
        name = cookie['name']
        value = cookie['value']
        mycookie += f'{name}={value};'
        print(mycookie)
        
    # 点击播放
    time.sleep(3)
    await page.click('.weui-audio-btn')
    
    audio = await page.Jeval('audio', 'el => el.src')
    print(audio)
    audioName = await page.Jeval(".audio_card_title", 'el => el.innerText')
    print(audioName)    
    
    response = requests.get(audio, headers={'cookie': mycookie, 'referer': audioUrl})

    storedPath = "AudioWebPy/"
    if not os.path.exists(storedPath):
        os.makedirs(storedPath)

    filename = f'{audioName}.mp3'
    filelocation = storedPath + filename
    with open(filelocation, 'wb') as f:
        f.write(response.content)
    print("FINISH")
     
    await browser.close()
    

if __name__ == '__main__':
    audioUrl = 'https://mp.weixin.qq.com/s/JrDd6y6Bb7Z63UCGO5mg9A'
    #getUrl()
    #asyncio.get_event_loop().run_until_complete(main(getUrl()))
    asyncio.run(main(audioUrl))
