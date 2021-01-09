###############################################################################
# describe: crawl Second Hand House infomation from Anjuke
# env: python3
# date: 20210108
# Author: 0xLiang
# thanks: jhao104/proxy_pool's author, https://github.com/jhao104/proxy_pool
###############################################################################


import requests
from bs4 import BeautifulSoup
import time
import random

# use proxy(docker fashion), from  jhao104/proxy_pool
def get_proxy():
    return requests.get("http://192.168.1.2:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://192.168.1.2:5010/delete/?proxy={}".format(proxy))

def getHtml(url, header):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            # 使用代理访问
            html = requests.get(url, headers=header, proxies={'http': 'http://{}'.format(proxy)}).content
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None

def parseHtml(html):
    global count
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find('ul',id='houselist-mod-new').find_all('li')
    with open('anjuke.csv', 'a', encoding='utf-8-sig') as f:
        for li in ul:
            count += 1
            # 总价
            priceTotal = li.find('div', class_='pro-price').find('span', class_='price-det').text.strip()
            # 每平方米价格
            pricePermm = li.find('div', class_='pro-price').find('span', class_='unit-price').text.strip()
            houseDetail = li.find_all('div', class_='house-details')
            for detail in houseDetail:
                title = detail.find('div', class_='house-title').text.strip()
#                 print(title)
                info = detail.find('span', class_='comm-address').text.strip()
                # 楼盘名称，“''.join(info.split())” 是为了 删除“&nbsp”
                name = ''.join(info.split()[0])
                # 楼盘地址
                addr = ''.join(info.split()[1])
                itemDetail = detail.find_all('div', class_='details-item')[0].find_all('span')
                # 户型
                roomNum = itemDetail[0].text.strip()
                # 户型面积
                houseSqr = itemDetail[1].text.strip()
                # 所属楼层
                high = itemDetail[2].text.strip()
                # 始建年份
                buildYear = itemDetail[3].text.strip()
            f.write(title)
            f.write(",")
            f.write(name)
            f.write(",")
            f.write(addr)
            f.write(",")
            f.write(roomNum)
            f.write(",")
            f.write(houseSqr)
            f.write(",")
            f.write(high)
            f.write(",")
            f.write(buildYear)
            f.write(",")
            f.write(priceTotal)
            f.write(",")
            f.write(pricePermm)
            f.write("\n")

# use random userAgent, for being antiCrawl
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
        'Cookie': 'sessid=538E9F42-71F0-D325-2CDE-11430F55B561; aQQ_ajkguid=E506583E-3B61-E547-48B0-7288DE6B6DCC; ctid=62; twe=2; id58=e87rkF/4JedkvxiMJKucAg==; wmda_uuid=a230f2d2df153b2efc54b275629471bb; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; browse_comm_ids=386794; ajk_member_captcha=5e4cb11917ce35a2b8cd2d9e04ce7f39; 58tj_uuid=eaca00a1-7a4a-46d5-8583-e3fac1cc1fad; als=0; propertys=2j15bzv-qmm6lg_2j0d99d-qmm06m_; isp=true; new_uv=2; wmda_session_id_6289197098934=1610118662276-87197029-ea42-f44e; obtain_by=1; xxzl_cid=7304624cfa4a4de088b619d8dfd22c1f; xzuid=ea9db5a7-424a-4aab-8a70-f484ab3cde5b'

        }
    return header
            
            
baseUrl = 'https://nanning.anjuke.com/sale/{}/p{}/'
zoneNanning = ['', 'qingxiu', 'xixiangtang', 'jiangnanxj', 'xingning', 'liangqing', 'yongning', 'wumingquwumingxian']
count = 0

if __name__ == '__main__':
    startTime = time.time()
    for zone in zoneNanning:
        print(f'begin crawl {zone}')
        for i in range(1,60):
            t = random.randint(1,2)
            url = baseUrl.format(zone, i)
            html = getHtml(url, getHeader())
            try:
                parseHtml(html)
                time.sleep(t)
            except:
                # print('have an error, continue')
                continue
    totalTime = time.time() - startTime
    print(f'一共爬取了{count}条数据, 耗时{totalTime}s')


    
    
    
    
    