##################################
# 获取南宁糖业新闻的标题和内容
# env: python3
# date: 20201216
# Author: 0xLiang
##################################

import requests
from bs4 import BeautifulSoup
import time

# 定义url，为后面和其他uri组成一篇文章完整的请求地址
url_old = 'http://tyfzb.gxzf.gov.cn/xwzx/zxzx/xhxh/'
news_count = 0

nowTime = time.strftime("%Y%m%d",time.localtime(time.time()))
fileName = "gxzfnews" + nowTime + '.txt'


# 爬取函数，此函数实现爬取请求地址中的所有标题和内容
def getNews(url):
    global news_count
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.27 Safari/537.36',
        'Cookie': '_trs_uv=kir6f8ky__henn; _trs_ua_s_1=kir6f8ky__a0ps; Hm_lvt_d12e9133f40a4dd7767eb68a8c55f0f2=1608108742; Hm_lpvt_d12e9133f40a4dd7767eb68a8c55f0f2=1608108742'
    }  
    
    # 对地址发起请求
    html = requests.get(url, headers=header).content
    # 使用BeautifulSoup解析获取到的内容
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    # 找出关于文章超链接，获取每个标题对应的uri
    # 通过div标签找出连接uri
#     divTag = soup.find_all('div', id='morelist')
    ulTag = soup.find_all('ul', class_='more-list')
    
#     print(divTag)
    for liTag in ulTag:
        ulTag = liTag.find_all('a')
        for a in ulTag:
            ul = a['href'][1:16]
#             print(ul)

    #         print(ul)
            # 把原始url和新获取的uri组合成单篇文章的具体地址
            url_real = url_old + ul
    #         print(url_real)
            # 对新地址发起请求
            html_real = requests.get(url_real, headers=header).content
            # 解析获取到的内容
            soup_real = BeautifulSoup(html_real, 'lxml', from_encoding='utf-8')
            # 通过div标签中的“article”，找出所有此div下所有内容
            divTag_real = soup_real.find_all('div', class_='article')

            # 打开一个txt文本
            f = open(fileName, mode='a', encoding='utf-8')

            # 获取新闻标题和内容
            for tag in divTag_real:
                # 获取标题
                news_title = tag.find('h1').get_text().strip()
                # 标题写入打开的文本中
                f.write(news_title)
                f.write("\n")
                # 爬取文章数统计
                news_count += 1
                # 通过div下的“view”属性更精确爬取文章
                div2 = tag.find('div', attrs={"class":["view"]})
                # 找出所有p标签(文本在p标签中)
                ptag = div2.find_all('p')
                # 获取文本
                for p in ptag:            
                    ptext = p.get_text().strip()
                    f.write(ptext)
                f.write("\n\n\n")
            f.close()
    

# 代码入口
if __name__ == '__main__':
    # 有4页新闻，找出这几页新闻的共同点，取出然后遍历，就可得到4页所有内容
    for i in ['index', 'index_1', 'index_2', 'index_3']:
        #找出url
        url_index = url_old + i + '.shtml'
#         print(url_index)
        # 调用爬取函数
        getNews(url_index)
    print(f' job done! 一共爬取了{news_count}篇文章,保存在{fileName}文件中')

    