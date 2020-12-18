### Docker install Selenium Grid for Python3 spider use

```
ENV: Win10, CentOS7
Author: 0xLiang
Date: 2020-12-19
Describe: 
   Coding(python) in CentOS7, Docker build Selenium Grid ENV，use VNC(in Win10) to monitor Selenium's process 
   在CentOS7编写Python爬虫，CentOS7下使用Docker创建Selenium Grid，在win10下使用VNC连接Selenium Grid，从而查看爬虫执行过程
```

##### *ENV*
> Python3.8
> Win10 ：192.168.123.1
> CentOS7: 192.168.123.2
> Docker Version: version 18.06.3-ce
> Docekr image: selenium/standalone-chrome:4.0.0-beta-1-prerelease-20201208

#### 1. Docker install Selenium Grid in CentOS7

Official doc: https://github.com/SeleniumHQ/docker-selenium
 
```
CentOS7(192.168.123.2):
]# Docker pull selenium/standalone-chrome:4.0.0-beta-1-prerelease-20201208
]# docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-1-prerelease-20201208
```

#### 2. Win10 connect Selenium Grid

- Win10 INSTALL Vncviewer(not mention here)
- Vncviewer connect Selenium Grid, "Service IP: 192.168.123.2:5900; default password:"secret"(no user name)

you will see the UI screen if it is success

#### 3. coding

example
```
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


driver = webdriver.Remote(
    command_executor = 'http://192.168.123.2:4444/wd/hub', 
    desired_capabilities = DesiredCapabilities.CHROME
)

driver.get('https://www.github.com')
time.sleep(5)
print(driver.page_source)
driver.close()

```
