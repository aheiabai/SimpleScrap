from pyppeteer import launch
import asyncio
import time
import requests
import os

async def main():
    audioUrl= 'https://mp.weixin.qq.com/s/JrDd6y6Bb7Z63UCGO5mg9A'
    # 启动一个浏览器
    browser = await launch(headless=False,args=['--disable-infobars'])
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
    
    response = requests.get(audio, headers={'cookie': mycookie,'referer': audioUrl})

    storedPath = "AudioWebPy/"
    if not os.path.exists(storedPath):
        os.makedirs(storedPath)

    filename = f'{audioName}.mp3'
    filelocation = storedPath + filename
    with open(filelocation, 'wb') as f:
        f.write(response.content)
    print("FINISH")
     
    await browser.close()
    
asyncio.get_event_loop().run_until_complete(main())