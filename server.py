# -*- coding: utf-8 -*-

import os, time
import sys
# import asciichart 
# import plot
# from asciichart import plot
# using datetime module
import datetime
# import flexmsg
import ccxt
import urllib.parse
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from flask import Flask, request, abort
#pip install line-bot-sdk
from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
#from linebot.models import (
#    TextSendMessage, FlexSendMessage
#)
#from linebot.models.template import *
#from linebot import (
#    LineBotApi, WebhookHandler
#)
import requests
import json
import subprocess

app = Flask(__name__)

binance = ccxt.binance({'enableRateLimit': True})
markets = binance.load_markets()

@app.route('/', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        #print(Reply_token)
        message = payload['events'][0]['message']['text']
        
        message = message.upper()
        cmd1 = f'python getData_binance.py {message}'

        # Using os.system() method
        os.system(cmd1)
        time.sleep(1)

        df = pd.read_csv('binance.csv')
        cmd2 = f'python getPrice.py {message}'
        
        last_price = subprocess.getoutput(cmd2)

        #Calculate the max and min close price
        maximum_price = df['close'].max()
        minimum_price = df['close'].min()
        difference = maximum_price - minimum_price #Get the difference        
        first_level = maximum_price - difference * 0.236   
        second_level = maximum_price - difference * 0.382  
        third_level = maximum_price - difference * 0.5     
        fourth_level = maximum_price - difference * 0.618  
        fifth_level = maximum_price - difference * 0.786

        url_picPlot = "https://forexreddit.com/wp-content/uploads/2020/03/wi3b3y9b.jpg"

        # if 'bitcoin' in message :
        if message in markets:    

            Reply_messasge = '''{"type": "bubble","header": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "%s","color": "#1DB446","size": "xxl","weight": "bold","align": "center"}],"backgroundColor": "#000000"},"body": {"type": "box","layout": "vertical","contents": [{"type": "box","layout": "vertical","contents": [{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "Last Price","color": "#000000","size": "lg","weight": "bold"},{"type": "text","text": "$%s","align": "end"}]},{"type": "separator","color": "#000000"}]},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "Fibonacci (%%)","size": "lg","weight": "bold"},{"type": "text","text": "($)","weight": "bold","size": "lg","align": "end"}],"borderColor": "#000000","paddingBottom": "sm","paddingTop": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "0","size": "sm","flex": 0},{"type": "text","text": "%s","size": "sm","color": "#111111","align": "end"}],"paddingStart": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "23.6","size": "sm","flex": 0},{"type": "text","text": "%s","size": "sm","color": "#111111","align": "end"}],"paddingStart": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "38.2","size": "sm","flex": 0},{"type": "text","text": "%s","size": "sm","color": "#111111","align": "end"}],"paddingStart": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "50","size": "sm","flex": 0},{"type": "text","text": "%s","size": "sm","color": "#111111","align": "end"}],"paddingStart": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "61.8","size": "sm","flex": 0},{"type": "text","text": "%s","size": "sm","color": "#111111","align": "end"}],"paddingStart": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "78.6","size": "sm","flex": 0},{"type": "text","text": "%s","size": "sm","color": "#111111","align": "end"}],"paddingStart": "xl"},{"type": "box","layout": "horizontal","contents": [{"type": "text","text": "100","size": "sm"},{"type": "text","text": "%s","size": "sm","color": "#000000","align": "end"}],"paddingStart": "xl"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "image","url": "%s","size": "full","aspectMode": "fit","aspectRatio": "10:3.65","backgroundColor": "#FFFFFF"},{"type": "button","action": {"type": "uri","uri": "%s","label": "Full Picture"},"style": "link"}],"paddingAll": "none","flex": 0},"styles": {"footer": {"separator": true}}}'''%(message,last_price,maximum_price,first_level,second_level,third_level,fourth_level,fifth_level,minimum_price,url_picPlot,url_picPlot)

            ReplyMessage(Reply_token,Reply_messasge,'2IQWSiweGIvQJAlWFtiElnrJHclALAadSbj9delCu8Iv2DQoWXsHO1/1YAHouQ6BYDlAS5oFz2x3Ui1s9mJswr1qqdBPmiKCLOaB+WvWkSmfEq7h26jiVmVpJIzZTVUBYtKZc6C0f/cvSkkm8lnLYgdB04t89/1O/w1cDnyilFU=',1)
            return request.json, 200
        else:
            Reply_messasge = f'Example: BTC/USDT'
            ReplyMessage(Reply_token,Reply_messasge,'2IQWSiweGIvQJAlWFtiElnrJHclALAadSbj9delCu8Iv2DQoWXsHO1/1YAHouQ6BYDlAS5oFz2x3Ui1s9mJswr1qqdBPmiKCLOaB+WvWkSmfEq7h26jiVmVpJIzZTVUBYtKZc6C0f/cvSkkm8lnLYgdB04t89/1O/w1cDnyilFU=',0)
            return request.json, 200
    else:
        abort(400)

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token, status):
    LineBOT = LineBotApi(Line_Acees_Token)
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    if status == 0:
        Reply_Obj = TextSendMessage(text=TextMessage)
    else:
        TextMessage = json.loads(TextMessage)
        Reply_Obj = FlexSendMessage(alt_text='Crypto Price :)', contents=TextMessage)
        
    LineBOT.reply_message(Reply_token, Reply_Obj)
    return 200
    

if __name__ == '__main__':
    app.run(debug=True)