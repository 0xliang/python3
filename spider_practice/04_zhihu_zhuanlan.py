#############################################################
# Describe: crawl "知乎专栏-慧田哲学人" from zhuanlan.zhihu.com
# ENV: python3
# Author: 0xLiang
# Date: 2021-01-07
# 
##############################################################


import requests
from lxml import etree

# 此函数实现每个页面内容的爬取，并保存到文件
# 1. 首先获取专栏首页文章的每个链接，对链接发起请求
# 2. 然后获取到每个具体请求的页面全部内容
# 3. 然后用lxml解析,获取文章标题和内容
def getAllUrl(url, header):
    # 使用request获取首页信息
    html = requests.get(url, headers=header).json()
    # 获取每个文章超链接(在json的['data']['url']下)
    allData = html['data']
    # 创建一个文件，为后面写入文章内容做准备
    with open('huitian_zhihu.txt', 'a', encoding='utf-8') as f:
        # 提取['data']列表里的每个['url']
        for ul in allData:
            url2 = ul['url']
            html2 = requests.get(url2, headers=header).text
            # 使用xpath分析, lxml模块
            tree = etree.HTML(html2)
            # 获取标题
            title = tree.xpath('//h1/text()')
            title = ''.join(title)
            # 标题格式化写入文件
            f.write("\n" * 3)
            f.write('TITLE<<')
            f.write(title)
            f.write('>>')
            f.write("\n" * 2)
            # 获取内容
            text = tree.xpath('//*[@id="root"]/div/main/div/article/div[1]/div//text()')
            # 换行，开头空两格
            text = '\n  '.join(text)
            f.write(text)
            f.write("\r\n")
            f.write('==' * 50)
    

# 起始链接
start_url = 'https://www.zhihu.com/api/v4/columns/cc2cc/items?limit=10&offset={}'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.50 Safari/537.36',
    'cookie': '_zap=7b33cda7-7a6f-4a22-b739-9b1c4c819993; _xsrf=46cd4872-74b4-4723-aaad-0e163521f0a3; d_c0="AOCfWvVSaxKPTt8iQPumgKnPPZU_5EUHahQ=|1609220040"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1609220047,1609307674,1609698153,1609814968; SESSIONID=8nvUVVHQw64dIxP86VnWINgfwHX1wh7FIOaENg8hDG5; JOID=VlgdB0Jo0eMCWCB7Q2goMl4YgR5dVLeZWgNyOx4S499qHFUvc9MGEV1RLH9CI0nGgNMX0EGNKPD8t1wqjF6_c6E=; osd=VV0XBEhr1OkBUiN-SWsiMVsSghReUb2aUAB3MR0Y4NpgH18sdtkFG15UJnxIIEzMg9kU1UuOIvP5vV8gj1u1cKs=; capsion_ticket="2|1:0|10:1609814990|14:capsion_ticket|44:M2Y5MmUyODVmNzJlNDY1MTk4NGQ1MWRlYjIzZTYwNDU=|c1d7f594f543216622d86c0ad446f4e92febf2e29795b09e928c8024e21889e3"; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1609815013; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1609815020|1609814962'
}


if __name__ == '__main__':
    # 分析链接格式，设置偏移量
    for i in range(7):
        offset = i * 10
        urlaaa = start_url.format(i)
        # 对链接发起请求，如果是有效链接，就调用函数
        # 如果链接无效，就跳出循环，结束爬取
        try:
            requests.get(url, headers=header)
        except:
            break
        else:
            getAllUrl(urlaaa, header)
    print("\n",'job done!')
        
        
        
