import json
import requests
import random
import time
from contextlib import suppress

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
                exchangeShortName = r['exchangeShortName']
                sector = r['sector']
        return mktCap,companyName,exchangeShortName,sector

def balanceSheetQuarter(symbol):
        response = requests.get('https://fmpcloud.io/api/v3/balance-sheet-statement/'+symbol+'?period=quarter&apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        for r in responseJson:
                m = 1000000
                fileDate = r['date']
                filePeriod = r['period']
                cashShortInv = r['cashAndShortTermInvestments'] / m
                totalLiabilities = r['totalCurrentLiabilities'] / m
                break
        return fileDate,filePeriod,cashShortInv,totalLiabilities

def keyMetricsQuarter(symbol):
        response = requests.get('https://fmpcloud.io/api/v3/key-metrics/'+symbol+'?period=quarter&apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        for r in responseJson:
                peRatio = round(r['peRatio'],2)
                pbRatio = round(r['pbRatio'],2)
                break
        return peRatio,pbRatio

def incomeStatementQuarter(symbol):
        response = requests.get('https://fmpcloud.io/api/v3/income-statement/'+symbol+'?period=quarter&apikey=8f763b9c95bd17444bbbd6c4f223988d')
        responseJson = json.loads(response.text)
        revenueDict = {}
        epsDict = {}
        counter = 0
        for r in responseJson:
                revenue = r['revenue'] / 1000000
                earnings = r['epsdiluted']
                revenueDict[str(counter)] = (revenue)
                epsDict[str(counter)] = (earnings)
                counter += 1
        return revenueDict,epsDict

stockScreener = {}
symList = masterSymbol()
#symList = ['AAPL','JPM']
for sym in symList:
        symbol = sym
        try:
                mktCap,companyName,exchangeShortName,sector = profile(symbol)
                fileDate,filePeriod,cashShortInv,totalLiabilities = balanceSheetQuarter(symbol)
                peRatio,pbRatio = keyMetricsQuarter(symbol)
                revenueDict,epsDict = incomeStatementQuarter(symbol)

        except:
                TypeError
                continue

        grahamNumber = peRatio * pbRatio
        liquidValue = cashShortInv - totalLiabilities

        try:
                priceLiquid = round(mktCap / liquidValue,2)
                #revenueTTMvsPTTM = round((revenueDict.get('0') + revenueDict.get('1') + revenueDict.get('2') + revenueDict.get('3')) / ((revenueDict.get('4') + revenueDict.get('5') + revenueDict.get('6') + revenueDict.get('7'))) - 1,2)
                #epsTTMvsPTTM = round((epsDict.get('0') + epsDict.get('1') + epsDict.get('2') + epsDict.get('3')) / ((epsDict.get('4') + epsDict.get('5') + epsDict.get('6') + epsDict.get('7'))) - 1,2)
                revenueTTMvsPTTM = round((revenueDict.get('0') + revenueDict.get('1') + revenueDict.get('2') + revenueDict.get('3')) / ((revenueDict.get('16') + revenueDict.get('17') + revenueDict.get('18') + revenueDict.get('19'))) - 1,2)
                epsTTMvsPTTM = round((epsDict.get('0') + epsDict.get('1') + epsDict.get('2') + epsDict.get('3')) / ((epsDict.get('16') + epsDict.get('17') + epsDict.get('18') + epsDict.get('19'))) - 1,2)
        except:
                ZeroDivisionError
                continue
        
        try:
                if priceLiquid <= .67 and priceLiquid >= .01:
                        stockScreener[str(symbol)] = (symbol,companyName,mktCap,exchangeShortName,sector,priceLiquid,revenueTTMvsPTTM,epsTTMvsPTTM)
                elif revenueTTMvsPTTM >= 0 and epsTTMvsPTTM >= 0 and grahamNumber >= 0 and grahamNumber <= 12:
                        print(symbol,fileDate,companyName,exchangeShortName,mktCap,sector,priceLiquid,revenueTTMvsPTTM,epsTTMvsPTTM,sep=',')
                        d = random.uniform(0,1)
                        time.sleep(d)
                else:
                        continue
        except:
                TypeError
                continue
print(stockScreener)