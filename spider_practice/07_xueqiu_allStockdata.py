###############################################################################
# describe: crawl all "A MARKET" Stock's history data from xueqiu.com
# env: python3
# date: 20210314
# Author: 0xLiang
# thanks:
###############################################################################



import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random
import json


def getHeader():
    """use random header
    """
    pc_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
    ]
    agent = random.choice(pc_agent)
    header = {
        'user-agent': agent
        }
    return header


def getHtml(startUrl, url, header):
    retry_count = 5
    # use Session, in order to get "requests cookie"
    session = requests.Session()
    session.get(startUrl, headers=header)
    while retry_count > 0:
        try:           
            html = session.get(url, headers=header).content
            return html
        except Exception as e:
            retry_count -= 1


def parseHtml(html):
    global count
    jsonData = json.loads(html)
    items = jsonData['data']['item']
    stocksymbol = jsonData['data']['symbol']
    stockName = jsonData['data']['symbol']
    for li2 in items: 
        count += 1
        # The Timestamp Result is not a Standard TimeStamp,
        # here do something to Convert it 
        timeStamp11 = int(str(li2[0])[:-3])
        timeStamp22 = time.localtime(timeStamp11)
        timeStamp = time.strftime("%Y-%m-%d", timeStamp22)
        volume = li2[1]
        closePrice = li2[5]
        upDownPercent = li2[7]
        turnoverRate = li2[8]
        amount = li2[9]
        pe = li2[12]
        pb = li2[13]
        ps = li2[14]
        marketCapital = li2[16]
        allData = [timeStamp, stockName, stocksymbol, volume, closePrice, upDownPercent, turnoverRate, amount, pe, pb, ps, marketCapital]
        insertDB(allData)

def insertDB(value):
    db = pymysql.connect(host="192.168.43.61", user="spider",
                         password="spider", db="spider", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO xqall (time, stockName, stocksymbol, volume, closePrice, upDownPercent, turnoverRate, amount, pe, pb, ps, marketCapital) VALUES (%s, %s, %s, %s, %s,  %s, %s,  %s, %s, %s,  %s, %s)"
    try:
        cursor.execute(sql,value)
        db.commit()
    except Exception as e:
        print("insert err! ", e, "\n", value)
        db.rollback()
        
    finally:
        cursor.close()
        db.close()



starUrl = 'https://www.xueqiu.com'
baseUrl = 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH601398&begin=946707878000&period=day&type=before&count=7200&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
count = 0

if __name__ == '__main__':
    startTime = time.time()
    html = getHtml(starUrl, baseUrl, getHeader())
    parseHtml(html)
    totalTime = time.time() - startTime
    print(f'Total get {count} info，cost {totalTime}')
