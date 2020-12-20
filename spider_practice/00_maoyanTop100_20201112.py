#################################################################################
# describe: this small web spider use to get top100 movie from maoyan.com
# env: python3
# author(practicer): 0xliang
# date: 12/11/2020
# thanks Cui Qingcai's book "Python3WebSpider"
#################################################################################



import requests
import re
import time
import json
from requests.exceptions import RequestException


def get_one_page(url):
    try:
      headers = {
          'Cookie': '__mta=216316585.1605184304467.1605191393629.1605191447424.6; uuid_n_v=v1; uuid=0319A30024E311EBB062B79AF17E21C12F443681B7D141F9900BACCC1209F678; _csrf=3191242d84d23d1fcb62a9465e11bcf26947c404bff19d8076b5950e44be27ec; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_cuid=175bc70a889c8-02af9875db30a7-c791c36-384000-175bc70a889c8; _lxsdk=0319A30024E311EBB062B79AF17E21C12F443681B7D141F9900BACCC1209F678; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1605184304; __mta=216316585.1605184304467.1605184304467.1605184304467.1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1605191445; _lxsdk_s=175bcc2d593-df2-36-da0%7C%7C7',
          'Host': 'maoyan.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
      }

      response = requests.get(url, headers=headers)
      if response.status_code == 200:
        return response.text
      return None
    except RequestException:
        return None

def parse_one_page(html):
#     print(html)
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
#     print(items)
    for item in items:
        yield {
            'idenx': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

        
def writeToFile(content):
    with open('miaoTop100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        
def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
#     result = parse_one_page(html)
#     print(html)
    for item in parse_one_page(html):
        print(item)
#     print(html)
        writeToFile(item)
    
if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1.5)
#     main(0)