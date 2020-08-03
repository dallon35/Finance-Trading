import json
import requests
import random
import time
import pandas as pd
import ta

# https://pythonbasics.org/multiple-return/
def masterSymbol():
        #from https://realpython.com/python-json/
        response = requests.get('https://fmpcloud.io/api/v3/stock/list?apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        symList = []
        for r in responseJson:
                symbol = r['symbol']
                symList.append(symbol)
        return sorted(symList)

def profile(symbol):
        response = requests.get('https://fmpcloud.io/api/v3/profile/'+symbol+'?apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        for r in responseJson:
                mktCap = r['mktCap'] / 1000000
                companyName = r['companyName']
        return mktCap,companyName

def tradingAlgo(symbol):
        response = requests.get('https://fmpcloud.io/api/v3/historical-price-full/'+symbol+'?serietype=line&apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        resJson = responseJson['historical']
        #https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        with open(symbol+'.json', 'w') as outfile:
            json.dump(resJson, outfile)
        rdf = pd.read_json(symbol+'.json')
        df = rdf.sort_index(ascending=False)
        #https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe
        j = len(df.index) - 2

        indicator_macd = ta.trend.MACD(close=df['close'])
        #df['macd'] = indicator_macd.macd()
        df['macd diff'] = indicator_macd.macd_diff()
        #df['macdsignal'] = indicator_macd.macd_signal()
        indicator_rsi = ta.momentum.RSIIndicator(close=df['close'])
        df['rsi'] = indicator_rsi.rsi()
        
        df.to_csv(symbol+'.csv',index=False)
        
        shares = 0
        balance = 0
        i = 0
        for i in range(i,j):
            macd = df.iat[i,2]
            rsi = df.iat[i,3]
            if macd < 0 and rsi < 100:
                #date = df.iat[i,1]
                #prevClose = df.iat[i-1,0]
                close = df.iat[i,0]
                #diff = round(((close / prevClose) - 1) * 100,4)
                shares += 100
                balance -= close * 100
                #print(date,close,diff,'buy',shares,round(balance,2))
                i += 1
            elif macd > 0 and rsi > 100:
                #date = df.iat[i,1]
                #prevClose = df.iat[i-1,0]
                close = df.iat[i,0]
                #diff = round(((close / prevClose) - 1) * 100,4)
                shares -= 100
                balance += close * 100
                #print(date,close,diff,'sell',shares,round(balance,2))
                i += 1
            else:
                i += 1
                continue
        final = round(-balance / shares,2)
        market = df.iat[i,0]
        return shares,balance,final,market

def dayTradingAlgo(symbol):
        response = requests.get('https://fmpcloud.io/api/v3/historical-chart/1hour/'+symbol+'?apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        #https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        with open(symbol+'.json', 'w') as outfile:
            json.dump(responseJson, outfile)
        rdf = pd.read_json(symbol+'.json')
        df = rdf.sort_index(ascending=False)
        #https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe
        j = len(df.index) - 2

        indicator_macd = ta.trend.MACD(close=df['close'])
        #df['macd'] = indicator_macd.macd()
        df['macd diff'] = indicator_macd.macd_diff()
        #df['macdsignal'] = indicator_macd.macd_signal()
        indicator_rsi = ta.momentum.RSIIndicator(close=df['close'])
        df['rsi'] = indicator_rsi.rsi()
        
        df.to_csv(symbol+'.csv',index=False)
        
        shares = 0
        balance = 0
        i = 0
        for i in range(i,j):
            macd = df.iat[i,6]
            rsi = df.iat[i,7]
            if macd < 0 and rsi < 100:
                #date = df.iat[i,1]
                #prevClose = df.iat[i-1,0]
                close = df.iat[i,0]
                #diff = round(((close / prevClose) - 1) * 100,4)
                shares += 100
                balance -= close * 100
                #print(date,close,diff,'buy',shares,round(balance,2))
                i += 1
            elif macd > 0 and rsi > 100:
                #date = df.iat[i,1]
                #prevClose = df.iat[i-1,0]
                close = df.iat[i,0]
                #diff = round(((close / prevClose) - 1) * 100,4)
                shares -= 100
                balance += close * 100
                #print(date,close,diff,'sell',shares,round(balance,2))
                i += 1
            else:
                i += 1
                continue
            i += 1
        final = round(-balance / shares,2)
        market = df.iat[i,0]
        return shares,balance,final,market

#symList = masterSymbol()
symList = ['SPY','VXX','SCHB','SCHA','SCHZ','SCHO']
for sym in symList:
    symbol = sym
    try:
        mktCap,companyName = profile(symbol)
    except:
        TypeError
        continue
    try:
        #shares,balance,final,market = dayTradingAlgo(symbol)
        shares,balance,final,market = tradingAlgo(symbol)
    except:
        KeyError
        continue
    if market / final != 0:
        print(symbol,companyName,shares,round(balance,2),final,market,sep=',')
    else:
        continue
    d = random.uniform(0,1)
    time.sleep(d)