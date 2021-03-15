# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


'''# 雪球json字段解释
    name: 股票名字
    symbol: 股票代码
	0	"timestamp": 时间
	1	"volume"： 成交量
	2	"open"： 开盘
	3	"high"： 最高
	4	"low"： 最低
	5	"close"： 收盘
	6	"chg"： 今日价格变动(和昨天比)
	7	"percent"： 今日涨跌幅
	8	"turnoverrate"： 换手率
	9	"amount"： 成交额
	10	"volume_post"
	11	"amount_post"
	12	"pe"： 市盈率
	13	"pb"： 市净率
	14	"ps"： 市销率
	15	"pcf"： 
	16	"market_capital"： 总市值
	17	"balance"
	18	"hold_volume_cn"
	19	"hold_ratio_cn"
	20	"net_volume_cn"
	21	"hold_volume_hk"
	22	"hold_ratio_hk"
	23	"net_volume_hk"

'''

class XueqiustockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    time = scrapy.Field()
    stockName = scrapy.Field()
    stocksymbol = scrapy.Field()
    volume = scrapy.Field()
    closePrice = scrapy.Field()    
    percent = scrapy.Field()
    turnoverRate = scrapy.Field()
    amount = scrapy.Field()
    pe = scrapy.Field()
    pb = scrapy.Field()
    ps = scrapy.Field()
    marketCapital = scrapy.Field()
