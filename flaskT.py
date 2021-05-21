'''
Created on May 14, 2021

@author: ahei
'''

from flask import Flask
from flask import request
import asyncio
import puppeteerTest
import threading
import logging



app = Flask(__name__)

logging.warning(threading.current_thread().name)
    
    
@app.route('/', methods = ['GET', 'POST'])
def hello():
    url = request.args['url']
    
    asyncio.run(puppeteerTest.main(url))

    return url

if __name__ == '__main__':
    app.run(host='localhost', port=7878, debug=False)
    



