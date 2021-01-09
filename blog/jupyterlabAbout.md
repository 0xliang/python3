### 关于jupyter的一些用法

- **安装**
  -  使用docker安装
     ```docker run -d --name notebook -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v /jupyter:/home/jovyan/work -u root jupyter/datascience-notebook```
     image: 使用的是jupyter/datascience-notebook
     JUPYTER_ENABLE_LAB=yes: 启用lab模式
     -v: 保存到宿主机目录，防止镜像停了之后文件丢失
     -u: root, 启用root，为后面安装selenium等做准备

- **安装插件**
  - jupyter-lsp插件
    插件作用：实现自动补全，安装好的jupyter没有自动补全功能
    1. 使用浏览器登录jupyter
    2. 插件栏启用
    3. 安装krassowski/jupyterlab-lsp
    4. `pip install  jupyterlab-lsp`
    5. `pip install python-language-server[all]`
    6. 



