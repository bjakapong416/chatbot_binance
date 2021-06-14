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
        print(Reply_token)
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

        # if 'bitcoin' in message :
        if message in markets:     
            Reply_messasge = f'{message} \rLast price: {last_price} \r\nFibonanci Level \r\n0%: {maximum_price} \r\n23.6%: {first_level} \r\n38.2%%: {second_level} \r\n50.0%: {third_level} \r\n61.8%: {fourth_level} \r\n78.6%: {fifth_level} \r\n100%: {minimum_price}'
            ReplyMessage(Reply_token,Reply_messasge,'2IQWSiweGIvQJAlWFtiElnrJHclALAadSbj9delCu8Iv2DQoWXsHO1/1YAHouQ6BYDlAS5oFz2x3Ui1s9mJswr1qqdBPmiKCLOaB+WvWkSmfEq7h26jiVmVpJIzZTVUBYtKZc6C0f/cvSkkm8lnLYgdB04t89/1O/w1cDnyilFU=')
            return request.json, 200
        else:
            Reply_messasge = f'Example: BTC/USDT'
            ReplyMessage(Reply_token,Reply_messasge,'2IQWSiweGIvQJAlWFtiElnrJHclALAadSbj9delCu8Iv2DQoWXsHO1/1YAHouQ6BYDlAS5oFz2x3Ui1s9mJswr1qqdBPmiKCLOaB+WvWkSmfEq7h26jiVmVpJIzZTVUBYtKZc6C0f/cvSkkm8lnLYgdB04t89/1O/w1cDnyilFU=')
            return request.json, 200
    else:
        abort(400)

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200

if __name__ == '__main__':



    app.run(debug=True)
