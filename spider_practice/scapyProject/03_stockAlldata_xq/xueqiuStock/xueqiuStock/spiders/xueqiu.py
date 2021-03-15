import scrapy
from xueqiuStock.items import XueqiustockItem
from copy import deepcopy
import json
import time

class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']

    def start_requests(self):
        headers = {
            'user-Agent':"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        }
        baseUrl = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
        for i in range(1, 145):
            url = baseUrl.format(i)
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.getStockCode
            )

    def getStockCode(self, response):
        item = XueqiustockItem()
        headers = {
            'user-Agent':"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        }
        detailUrl = 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin=946707878000&period=day&type=before&count=7200&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
        jsonData = json.loads(response.text)
        lists = jsonData['data']['list']
        for li in lists:
            stockCode = li['symbol']
            item['stockName'] =  li['name']
            item['stocksymbol'] = stockCode
            realUrl = detailUrl.format(stockCode)
            yield scrapy.Request(
                url=realUrl,
                headers=headers,
                callback=self.getStockDetail,
                meta={'item':deepcopy(item)}
            )
    
    def getStockDetail(self, response):
        item = response.meta['item']
        jsonData = json.loads(response.text)
        items = jsonData['data']['item']
        for li2 in items:
            timeStamp11 = int(str(li2[0])[:-3])
            timeStamp22 = time.localtime(timeStamp11)
            item['time'] = time.strftime("%Y-%m-%d", timeStamp22)
            item['volume'] = li2[1]
            item['closePrice'] = li2[5]
            item['percent'] = li2[7]
            item['turnoverRate'] = li2[8]
            item['amount'] = li2[9]
            item['pe'] = li2[12]
            item['pb'] = li2[13]
            item['ps'] = li2[14]
            item['marketCapital'] = li2[16]
            # allData = [timeStamp, item['stockName'], item['stocksymbol'], volume, closePrice, upDownPercent, turnoverRate, amount, pe, pb, ps, marketCapital]
            # print(allData)
            yield item



            
