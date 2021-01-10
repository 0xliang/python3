###############################################################################
# describe: crawl Second Hand House infomation from fang.com
# env: python3
# date: 20210109
# Author: 0xLiang
# thanks: jhao104/proxy_pool's author, https://github.com/jhao104/proxy_pool
###############################################################################

import requests
from lxml import etree
import time
import random
import pandas as pd

def get_proxy():
    return requests.get("http://192.168.1.2:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://192.168.1.2:5010/delete/?proxy={}".format(proxy))

def getHtml(url, header):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            # 房天下有反爬，首页会自动302重定向
            # 这里要取出重定向地址，再根据这个地址爬取
            result = requests.get(url, headers=header)
            result.encoding='utf-8'
            reHtml = result.text
            reUrl = re.search('//location.href=\"(.*?)\"\;', reHtml)
            if reUrl:
                newUrl = reUrl.group(1)
                print(newUrl)
            html = requests.get(newUrl, headers=header, proxies={'http': 'http://{}'.format(proxy)})
#             print(html)
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None

pdListUse = []

def parseHtml(html):
    global count
    # pandas的格式定义，还不太熟，先抄网上的方法使用
    titles = []
    names = []
    zones = []
    layouts = []
    squares = []
    Heights = []
    directions = []
    buildTimes = []
    totalPrices = []
    perMMs = []
    e = etree.HTML(html)
    itemList = e.xpath('//div[@class="shop_list shop_list_4"]/dl')
    for item in itemList:
        count += 1
        # 获取标题名称
        title = item.xpath('.//h4/a/span/text()')
        title = ''.join(title).strip()
        # 获取小区名称
        name = item.xpath('.//p[@class="add_shop"]/a//text()')
        name = ''.join(name).strip()
        # 获取小区所属区域
        zone = item.xpath('.//p[@class="add_shop"]/span//text()')
        zone = ''.join(zone).strip()
        # 获取房子信息    
        houseDetail = item.xpath('.//p[@class="tel_shop"]/text()')
        if houseDetail:
            layout = houseDetail[0].strip()
            square = houseDetail[1].strip()
            Height = houseDetail[2].strip()
            direction = houseDetail[3].strip()
            buildTime = houseDetail[4].strip()
#             print(layout, square, Height, direction, buildTime)
        else:
            continue
       # 获取总价
        totalPrice = item.xpath('.//dd[@class="price_right"]/span[@class="red"]//text()')
        totalPrice = ''.join(totalPrice).strip()
        # 获取单价
        perMM = item.xpath('.//dd[@class="price_right"]/span[2]//text()')
        perMM = ''.join(perMM).strip()
        houseResult = {
            'title': title,
            'name' : name,
            'zone' : zone,
            'layout': layout,
            'square': square,
            'Height': Height,
            'direction': direction,
            'buildTime': buildTime,
            'totalPrice': totalPrice,
            'perMM': perMM
        }
        titles.append(title)
        names.append(name)
        zones.append(zone)
        layouts.append(layout)
        squares.append(square)
        Heights.append(Height)
        directions.append(direction)
        buildTimes.append(buildTime)
        totalPrices.append(totalPrice)
    resultData = {
        'title': titles,
        'name' : names,
        'zone' : zones,
        'layout': layouts,
        'square': squares,
        'Height': Heights,
        'direction': directions,
        'buildTime': buildTimes,
        'totalPrice': totalPrices,
        'perMM': perMM
    }
    df = pd.DataFrame(data=resultData, columns=['title', 'name', 'zone', 'layout', 'square', 'Height', 'direction', 'buildTime', 'totalPrice', 'perMM'])
    df.to_csv('fangTianXia_nn_333.csv', mode='a', index=False, header=False)
        
#         print(title, name, zone, layout, square, Height, direction, buildTime, totalPrice, perMM)
#         print("\n")
        
      

def getHeader():
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
        'user-agent': agent,
        'Cookie': 'global_cookie=9xk3e8ug5ointyn2rp5fjdg4z10kjpwix6r; unique_cookie=U_9xk3e8ug5ointyn2rp5fjdg4z10kjpwix6r*6; csrfToken=QgiB-zefAAGIGCYSKu4Y9SMR; g_sourcepage=esf_fy%5Elb_pc; city=nn'
        }
    return header
            
            
baseUrl = 'https://nn.esf.fang.com/house/i3{}'


# zoneNanning = ['', 'qingxiu', 'xixiangtang', 'jiangnanxj', 'xingning', 'liangqing', 'yongning', 'wumingquwumingxian']
setColumn = ['title', 'name', 'zone', 'layout', 'square', 'Height', 'direction', 'buildTime', 'totalPrice', 'perMM']
count = 0

if __name__ == '__main__':
    startTime = time.time()
    for i in range(1,100):  
        t = random.randint(0,2)
        url = baseUrl.format(i)        
        result = getHtml(url, getHeader())
        result.encoding='utf-8'
        html = result.text
        time.sleep(t)

    totalTime = time.time() - startTime
    print(f'一共爬取了{count}条数据, 耗时{totalTime}s')


    
    
    
    
    