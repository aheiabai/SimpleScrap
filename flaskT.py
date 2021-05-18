'''
Created on May 14, 2021

@author: ahei
'''

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"




