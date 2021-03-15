# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class mysqlPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(
            host = '192.168.43.61',
            port = 3306,
            db = 'spider',
            user = 'spider',
            passwd = 'spider'
        )
        self.cursor = self.db.cursor()


    def process_item(self, item, spider):
        timeStamp = item['time']
        stockName = item['stockName']
        stocksymbol = item['stocksymbol']
        volume = item['volume']
        closePrice = item['closePrice']
        upDownPercent = item['percent']
        turnoverRate = item['turnoverRate']
        amount = item['amount']
        pe = item['pe']
        pb = item['pb']
        ps = item['ps']
        marketCapital = item['marketCapital']
        sql = """
                INSERT INTO xqall 
                ( time, stockName, stocksymbol, volume, closePrice, upDownPercent, turnoverRate, amount, pe, pb, ps, marketCapital) 
                VALUES
                ('{}', '{}', '{}', '{}', '{}',  '{}', '{}',  '{}', '{}', '{}',  '{}', '{}')""".format(timeStamp, stockName, stocksymbol, volume, closePrice, upDownPercent, turnoverRate, amount, pe, pb, ps, marketCapital)
        self.cursor.execute(sql)
        self.db.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
