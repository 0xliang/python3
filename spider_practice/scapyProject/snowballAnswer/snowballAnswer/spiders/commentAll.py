# coding = 'utf-8'

import scrapy
import json
import copy
from snowballAnswer.items import SnowballanswerItem

class CommentallSpider(scrapy.Spider):
    name = 'commentAll'
    allowed_domains = ['xueqiu.com']
    baseCodeUrl = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=US&type=us&'
    # start_urls = ['http://xueqiu.com/']
    baseCommentUrl = 'https://xueqiu.com/query/v1/symbol/search/status?u=181609180312201&uuid=1343800227613786112&count=10&comment=0&symbol={}&hl=0&source=all&sort=time&page={}&q=&type=0&session_token=null&access_token=ad26f3f7a7733dcd164fe15801383e62b6033003'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.50 Safari/537.36'
    }

    def start_requests(self):
        for i in range(1, 300):
            url = self.baseCodeUrl.format(i)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    # 爬取所有股票代码，并把代码通过“meta”传给cmParseFirst
    def parse(self, response):
        codeHtml = response.json()
        listaaa = codeHtml['data']['list']
        stockCount = codeHtml['data']['count']
        item = SnowballanswerItem()
        for i in range(1, 300):
            if i*30 < stockCount:
                for info in listaaa:
                    codeName = info['symbol']
                    item['stockCode'] = codeName
                    # print(codeName)
                    # stockName = info['name']                
                    # yield stockCode
                    for j in range(10):
                        urlcomment = self.baseCommentUrl.format(codeName, j)
                        yield scrapy.Request(urlcomment, headers=self.headers, callback=self.cmParseFirst, meta={'item': copy.deepcopy(item)})



    # 通过股票代码，根据网页分析的每个股票“评论内容”的url，拼接成地址
    def cmParseFirst(self, response):
        item2 = response.meta['item']
        html = response.json()
        listaaa = html['list']
        for li in listaaa:
            item2['cmUserName'] = li['user']['screen_name']
            item2['stockComment'] = li['text']
            yield item2


    # def cmParseSec(self, response):
    #     item3 = response.meta['item2']
    #     html3 = response.json()
    #     cmCount = html3['count']
    #     for i in range(cmCount):
    #         cmUrlSec = self.baseCommentUrl.format(item3['codeName'], i)
    #         yield scrapy.Request(cmUrlSec, headers=self.headers, callback=self.cmParseThd, meta={'item3':copy.deepcopy(item3)})

    # def cmParseThd(self, response):
    #     pass


    
        
