# coding: utf-8
import scrapy
import re
import json
from stockEastmoney.items import StockeastmoneyItem

class StockspiderSpider(scrapy.Spider):
    name = 'stockSpider'
    allowed_domains = ['eastmoney.com']
    baseUrl = 'http://quote.eastmoney.com/center/gridlist.html#hs_a_board'
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    }

    
    def start_requests(self):
        start_url = 'http://62.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408670766297407351_1608804425602&pn={}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&'
        for i in range(1,201):
            urlReal = start_url.format(i)
            yield scrapy.Request(url=urlReal)

    

    def parse(self, response):
        try:
            item = StockeastmoneyItem()
            html = re.findall(r"\{.*\}", response.text)
            htmlJson = json.loads(html[0])
            stockData = htmlJson['data']['diff']
            for _item in stockData:
                item['lastPrice'] = _item['f2']
                item['stockName'] = _item['f14']
                item['stockCode'] = _item['f12']
                yield item
        except:
            print('aaaaaaa Error, Check it pls')
