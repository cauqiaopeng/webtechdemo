# web技术及数据获取与处理实训

> 作者：乔鹏、张钦

实训目标：

+ 掌握GitHub协同开发
+ 掌握Web爬虫的基本流程
+ 实现获取网站数据
+ 掌握数据可视化工具

## 一、基础知识及网站分析

### 1、工具包

```python
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
```

> **Requests**  是用Python语言编写，基于 urllib，采用 Apache2 Licensed 开源协议的 HTTP 库。它比 urllib 更加方便，可以节约我们大量的工作，完全满足 HTTP 测试需求。Requests 的哲学是以 PEP 20 的习语为中心开发的，所以它比 urllib 更加 Pythoner。更重要的一点是它支持 Python3 哦！

> **Beautiful Soup** 是一个可以从 HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航，查找，修改文档的方式。**Beautiful Soup** 会帮你节省数小时甚至数天的工作时间。

### 2、Python的安装及开发环境

采用`Python`语言进行数据获取。

推荐使用`Anaconda`作为`python`的包管理器和环境管理器，使用 `Jupyter notebook`作为日常数据分析的工具。

本教程使用`Pycharm` 作为项目的集成开发环境。学生可使用`cau.edu.cn` 的邮箱获取一年的免费使用权。

Windows与Mac系统的环境配置略有不同，但都属于基础操作，这里不赘述。

> python的安装及配置参照：https://www.runoob.com/python/python-install.html
>
> pycharm的下载地址：https://www.jetbrains.com/pycharm/

### 3、GitHub使用

>GitHub是通过Git进行版本控制的软件源代码托管服务平台，由GitHub公司的开发者Chris Wanstrath、PJ Hyett和Tom Preston-Werner使用Ruby on Rails编写而成。 GitHub同时提供付费账户和免费账户。

#### 3.1 环境准备

+ 注册 GitHub 账号

进入 [GitHub ⽹站](https://github.com/) 注册⼀个⾃⼰的账户

`https://github.com/your-account` 就是你 Github 的首页。你所有的文档、代码及其历史都保存在其中的仓库（Repositories ）中。

+ 安装 git 管理⼯具

从 [git 工具官⽹](https://git-scm.com/downloads) 直接下载安装程序，按提示选择合适系统安装。

+ 新建GitHub账户

按照GitHub系统提醒，注册用户即可。记住用户名密码。

+ 在pycharm中配置

需要在pycharm中配置git、GitHub相关信息。

#### 3.2GitHub使用

在GitHub新建一个`Repositories`（仓库），然后在pycharm中`clone`这个项目。之后就可以在本地开始coding了。

登录GitHub网站后，在右上角点击【+】，选择【New Repositories】即可。按照提示操作，输入项目名称。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gg145gerhnj30sw0l0acm.jpg" alt="image-20200622154707715" style="zoom:33%;" />

新建好`Repositories`后，回到pycharm，在【VCS】-【checkout from version control】中clone这个项目。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gg148lqwkuj31660nikcg.jpg" alt="image-20200622155008843" style="zoom: 50%;" />

> 参见材料：
>
> >  PyCharm 配置 Git 教程: https://cloud.tencent.com/developer/article/1478265
> >
> > git及GitHub教程：https://www.liaoxuefeng.com/wiki/896043488029600/900937935629664

## 二、目标网站分析

### 1、数据源网站

农机360网-购置补贴查询系统

> http://butie.nongji360.com/

![image-20200622152401522](https://tva1.sinaimg.cn/large/007S8ZIlly1gg13hg67bmj318v0u0wu6.jpg)

### 2、网站分析

对于一个软件项目，在开始coding之前，我们要思考系统的需求是什么，要达到什么目的。同样，在编写爬虫之前，我们需要先思考爬虫需要干什么、目标网站有什么特点，以及根据目标网站的数据量和数据特点选择合适的架构。

推荐使用Chrome的开发者工具来观察网页结构。在OS X上，通过`option+command+i`可以打开Chrome的开发者工具，或者通过**视图** -**开发者** 进入开发者模式。在Windows和Linux，对应的快捷键是"F12"。

![image-20200620230729245](https://tva1.sinaimg.cn/large/007S8ZIlly1gg142qyxofj30zs0k0e09.jpg)

通过观察网页 ，我们会发现，需要的数据都展示在表格当中。通过开发者工具，可以看到这个表格的标签是 `<table>`  。因此，在获取数据的时候，我们只需要这个`<table>` 标签下的内容即可。

![image-20200620231547393](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1436dit0j31850u0dp8.jpg)

针对表格内的每一行数据进行分析，可以看到，每一行的标签是`<tr>` ，每个单元格的标签是`<td>` 。

![image-20200620232013335](https://tva1.sinaimg.cn/large/007S8ZIlly1gg143tvciuj31le0s0wlp.jpg)

下一步我们针对**分页** 进行分析。我们可以看到，分页内容全都在一个`<id_page_def>` 标签下，每一页都是一个`<a>` 标签，而尾页是在最后一个`<a>` 内。所以，我们可以通过这两个标签获取到所有的分页。

![image-20200620232501962](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1440sdu3j31hu0u07d7.jpg)

截止目前，我们具备了获取针对某个城市的所有补贴数据的信息。那么，对于不同的城市如何处理？现在我们针对不同的城市进行分析。我们可以看到，在页面上有一个选择城市的选项。

通过开发者工具，我可以看到，城市的选择都是在一个`<tiaojian_list>` 的标签下，每个城市都有一个`<a>` 标签，`<a>` 标签内有一个链接，`text`内容是这个城市的名字。因此，我们可以通过这两个标签，获取到所有的城市。同时，通过观察可以看到，这里`<a>`标签内的链接，恰好就是对应到这个城市的URL。

![image-20200620233314109](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1445lidvj31qk0u0jzv.jpg)

我们已经完成了网页内容的大概分析，对如何进行获取数据也有了基本的思路。

## 三、爬虫的代码实现

### 1、下载网页源代码

第一步 ，我们先下载目标网页的源代码，使用的库是`requests`库。

```python
def downloadPage(url):
    # 下载页面方法，用requests模块，使用代理，避免重复请求次数过多
    headers = {
        'Content-Type':'text/html; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36' }
    data = requests.get(url, headers=headers).text
    return data
```

这里我们用的URL是某一个城市的页面地址，http://butie.nongji360.com/catalog/index/anhui。为避免访问次数过多，我们使用 `User-Agent`，中文名为用户代理，简称 UA。它是一个特殊字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等。网站可以通判断 UA 来给不同的操作系统、不同的浏览器发送不同的页面，对于爬虫来说，UA就是标明身份的第一层标识。

通过 `downloadPage`函数，我可以获取到网页的源代码，如果把它打印出来，其结果如下：

![image-20200621094255996](/Users/qiaopeng/Library/Application Support/typora-user-images/image-20200621094255996.png)

### 2、获取目标表格中的数据

这一步，我们要获取目标表格中的数据，使用的库是`BeautifulSoup`。

>**Beautiful Soup**是一个Beautiful Soup是一个Python包，功能包括解析HTML、XML文档、修复含有未闭合标签等错误的文档（此种文档常被称为tag soup）。这个扩展包为待解析的页面创建一棵树，以便提取其中的数据，这在网络数据采集时非常有用。

```python
def getData(url):
    # 获取表格中的数据，找到有用的几个信息，品目、分档、补贴
    content = downloadPage(url)
    print(content)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find('table').findAll('tr')
    pageDatas = []
    for i in list:
        tds = i.findAll('td')
        if (len(tds) == 0):
            continue
        if (len(tds)<4):
            continue
        pinmu = tds[1].get_text()
        fendang = tds[2].get_text()
        butie = tds[3].get_text()
        res = {
            "pinmu":pinmu,
            "fendang":fendang,
            "butie":butie
        }
        pageDatas.append(res)
    return pageDatas
```

通过我们之前对网页的分析可以看出，表格的内容都在`<table>`标签下，而且整个源代码只有一个`<table>`标签。具体某一个单元格的数据可以通过`<tr>`和`<td>`这两个标签获取。

通过 `getData`函数，我可以获取到某个网页的表格数据，如果把它打印出来，其结果如下：

![image-20200621095037777](/Users/qiaopeng/Library/Application Support/typora-user-images/image-20200621095037777.png)

### 3、获取表格的全部分页

在获取表格的数据的时候，我们发现，当前页面仅显示一部分的数据，要获取到所有分页的数据，仍需要知道有多少页数据，并且找到每页数据与对应的URL之间的规律。

```python
def getPageSize(url):
    # 获取表格的分页总数
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find('div', attrs={"id":"id_page_def"}).findAll("a")
    return int(list[-1].attrs['page'])
```

通过我们之前对网页的分析可以看出，分页栏的内容都在`<id_page_def>`标签下，而且整个源代码只有一个`<id_page_def>`标签。每个页面对应一个`<a>`标签，尾页是在最后一个`<a>`标签中。

通过`getPageSize`函数，我们获取到了某一个页面中，表格的所有页码，也就是表格对应的尾页是多少。

### 4、获取城市列表

这一步，我们要获取所有城市的数据，并且找到每个城市的数据与对应的URL之间的规律。这样，我们就可以获取到全国的农机购置补贴的数据了。

```python
def getCityList(url):
    # 获取所有的城市信息列表
    cityList = []
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find("div", attrs={"class":"tiaojian_list"}).findAll("div")
    listA = list[0].findAll('a')
    for a in listA:
        name = a.get_text()
        href = a.attrs['href']
        cityList.append({'href':href, 'name':name})
    return cityList
```

通过我们之前对网页的分析可以看出，城市数据内容都在`<tiaojian_list>`标签下，而且整个源代码只有一个`<tiaojian_list>`标签。每个城市的数据对应一个`<a>`标签。

通过`getCityList`函数，我们获取到了这个网站中所有的城市数据。如果把这个函数的内容打印出来，结果如下：

![image-20200621100454020](/Users/qiaopeng/Library/Application Support/typora-user-images/image-20200621100454020.png)

### 5、获取全部城市的目标数据

这是最后一步，我们通过之前的函数，已经实现下载网页源代码、获取表格中的数据、获取表格的分页数、获取全部城市的信息。现在，我们就要实现一次性获取全部城市的购置补贴数据。

```python
def downAllDatas():
    # 下载所有城市的数据
    url = "http://butie.nongji360.com/catalog/index/anhui"
    citylist = getCityList(url)
    for city in citylist:
        cityHref = baseUrl+city.get('href')
        cityData = []
        pageSize = getPageSize(cityHref)
        i = 1
        while(i < pageSize):
            pageDatas = getData(cityHref+"?p"+str(i))
            cityData.extend(pageDatas)
            i += i
        datas[city.get('name')] = cityData
    return datas
```

 其中，`baseUrl`和`datas`是定义的两个全局变量，分别表示是要查询的目标基础URL和存储查询结果数据。

截止目前，我们就完成了农机购置补贴数据的获取，获取结果我们存在JSON中，打印出来可以看到如下结果。

![image-20200621101525921](/Users/qiaopeng/Library/Application Support/typora-user-images/image-20200621101525921.png)

## 四、数据可视化开发

### 1、Echarts使用

### 2、MySQL使用

### 3、数据可视化Web系统开发



