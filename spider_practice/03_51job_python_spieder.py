#########################################
# Describe: get job's info from 51job 
# ENV: python3
# Author: 0xLiang
# Date: 2020-12-20
# 
#########################################





from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from time import sleep
import os



'''
此函数分析页面内容，并把内容写入到csv文件中
'''
def getJob(html):
    soup = BeautifulSoup(html, 'lxml')
    jobss = soup.find_all('div', class_='j_joblist')
    f = open('jobs51_dveops_20201220_4.csv', mode='a', encoding='utf-8-sig')
    for div in jobss:
        job = div.find_all('div', class_='e')
        for item in job:
            jobName = item.find('span', class_='jname at').text
            f.write(jobName)
            f.write(',')
            salary = item.find('span', class_='sal').text
            f.write(salary)
            f.write(',')
            company = item.find('a', class_='cname at').text
            f.write(company)
            f.write(',')
            location = item.find('span', class_='d at').text.split('|')[0]
            if location.split('-'):
                location = location.split('-')[0]
            f.write(location)
            f.write(',')
            link = item.a['href']         
            f.write(link)
#             print(jobName,"\t", salary,"\t", company, "\t", location)
            f.write("\n")
    f.close()



# 使用Chrome的“headless”模式爬取(用可视化调试好后的代码)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 禁止追踪
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=chrome_options)

## 这段是调用selenium Grid, 在远程打开调试窗口
# remote selenium
# browser = webdriver.Remote(
#     command_executor = 'http://192.168.123.123:4444/wd/hub', 
#     desired_capabilities = DesiredCapabilities.CHROME
# )

# 给定url
url = 'https://www.51job.com/'
    
browser.get(url)
sleep(3)

# 找到“登录”按钮，并点击
browser.find_element_by_xpath("//p[@class='op']/a[1]").click()
phone = browser.find_element_by_xpath('//input[@placeholder="请输入手机号码/邮箱/用户名"]')
pwd = browser.find_element_by_xpath('//input[@placeholder="请输入密码"]')
# 输入账号
phone.clear()
phone.send_keys('13100000000')
# 输入密码
pwd.clear()
pwd.send_keys('1234567')
# 取消自动登录前的“勾”
browser.find_element_by_xpath("//*[@id='signup']/div[5]/label").click()
# 找到“登录”，并点击
browser.find_element_by_xpath("//*[@id='login_btn']").click()  

sleep(3)

# 找到“首页”，并点击
browser.find_element_by_xpath("//*[@id='topIndex']/div/p/a[1]").click()
# 找到“搜索栏”
search1 = browser.find_element_by_xpath("//*[@id='kwdselectid']")
search1.clear()
# 输入“关键字”
search1.send_keys('运维')
# 找到“地址”，此处操作实现爬取全国的信息
search_location = browser.find_element_by_xpath("//*[@id='work_position_input']")
search_location.click()
curr_location = browser.find_element_by_xpath("//*[@id='work_position_click_multiple_selected_each_140200']/span")
if curr_location:
    curr_location.click()
browser.find_element_by_xpath("//*[@id='work_position_click_bottom_save']").click()
sleep(1)
# 找到地址栏搜索按钮，并点击
submit = browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/button")
submit.click()
sleep(3)

# 获取网页返回数据
html11 = browser.page_source
# 调用自定义函数“getJob”， 获取页面数据
getJob(html11)

# 写个死循环，让程序一直爬取，知道异常退出为止(此处为了测试用，并无恶意)
# 此次运行一共爬取了6w多条数据
# 验证发现，51job的反爬措施比拉勾做得差，但对获取信息的我们来说是友好的
while True:
    # 找到“next”按钮，并点击
    next1 = browser.find_element_by_xpath("//ul/li[@class='next']")
    next1.click()
    sleep(5)
    # 调用自定义函数getJob获取数据
    getJob(browser.page_source)
    
browser.close()