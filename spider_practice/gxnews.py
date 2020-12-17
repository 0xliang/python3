#############################
#
# 代码作用：爬取广西糖业新闻，并保存到当前目录下“gxnewsaaa.txt”文件中
# env: python3
# time: 2020-12-12
#
############################


# 使用“requests”和“BeautifulSoup”模块
import requests
from bs4 import BeautifulSoup




# 定义初始url，后面url拼接时用到
url_begin = 'http://www.gxnews.com.cn'

# 爬虫开始爬取的url
url = 'http://www.gxnews.com.cn/staticmores/510/46510-1.shtml'
# 设定请求头部，伪装成普通浏览
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.27 Safari/537.36',
    'Cookie': 'UM_distinctid=1765650e8b524f-03b0c1d7ea2b6c-8761b3c-384000-1765650e8b6252; CNZZDATA30019958=cnzz_eid%3D1963308582-1607763398-null%26ntime%3D1607763398; Hm_lvt_2620280f16ac55aff03ddc777d6c29da=1607765915,1607765976; Hm_lpvt_2620280f16ac55aff03ddc777d6c29da=1607765976'
}

# 获取页面数据
html = requests.get(url, headers=header).content

#使用Beautiful实例化对象
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# 找出关于文章超链接，获取每个标题对应的uri
ulTag = soup.find('ul', class_='more-list').find_all('li')

# 获取文章uri，然后与初始url拼接，成为一个完整文章url
# 即：“http://www.gxnews.com.cn” + “staticpages/20201127/newgx5fc0730f-19964440.shtml”
# 文章完整的url： http://www.gxnews.com.cn/staticpages/20201127/newgx5fc0730f-19964440.shtml
for li in ulTag:
    url_a = li.a['href']
    url_new = url_begin + url_a
    html_real = requests.get(url_new, headers=header).content
    soup_real = BeautifulSoup(html_real, 'html.parser', from_encoding='utf-8' )
    
    divTag_npic = soup_real.find_all('div', attrs={"class":["more-left","page_content"]} )
    
    
    for tag in divTag_npic:
        #获取文章标题
        news_head = tag.find('h1').get_text()
        print(news_head.strip())
#         with open('gxnewsaaa.txt', 'a', encoding='utf-8') as f1:
#             f1.write('\n'.join([news_head]))

        # 获取文章内容
        ptag = tag.find_all('p')
        for pText in ptag:
            news_text = pText.get_text()
            print(news_text,end='')
#             with open('gxnewsaaa.txt', 'a', encoding='utf-8') as f2:
#                 f2.write(news_text)
#         with open('gxnewsaaa.txt', 'a', encoding='utf-8') as f3:
#             f3.write('\n' + '=' * 50 + '\n\n')
        print("\n\n")
            
            
print("\n\n", 'job done!')