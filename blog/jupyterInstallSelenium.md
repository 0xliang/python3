### Use selenium in jupyter

```
ENV: CentOS7, Docker
TIME: 2020-12-17
Author: 0xLiang
Describe: Use Selenium in Jupyter,just for person use, not recommend in product environment
```

#### Build your own Platform
1. CentOS7

    `Not mention here`

2. Install Docker

    `Not mention here`

3. Docker install Selenium

        Docker image: `jupyter/datascience-notebook:latest`


#### Install selenium

**prepara:**

* Chrome: google-chrome-stable_current_amd64.deb
* chromedriver


*note: chrome and chromedriver must be the same VERSION, hear use "Google Chrome 86.0.4240.198"*


**First**
1.1 Run image: `docker run -d --name notebook -p 8888:8888 -v /some/path/jupyter:/home/jovyan/work -u root jupyter/datascience-notebook start-notebook.sh --NotebookApp.password='yourpasswd'`
1.2 open jupyter
1.2 pip install selenium

**Second**

2.1 copy Chrome and chromedriver into the image
`docker cp google-chrome-stable_current_amd64.deb  6c7c3d0c3f74:/home/jovyan/work`
`docker cp  chromedriver 6c7c3d0c3f74:/home/jovyan/work`
2.2 get inside the docker image 
```
]# docker exec -it -u root 6c7c3d0c3f74 /bin/bash
(base) root@6c7c3d0c3f74:~# chmod 755 chromedriver
(base) root@6c7c3d0c3f74:~# mv /home/jovyan/chromedriver /usr/local/bin/
```

#### Use selenium 

Switch to jupyter
open http://youip:8888 in your web

Test code:
```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(options=chrome_options)
url = 'https://github.com/'
browser.get(url)
html = browser.page_source
print(html)

```






