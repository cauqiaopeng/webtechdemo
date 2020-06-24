# web技术及数据获取与处理实训

[toc]

***



> 作者：乔鹏、张钦



实训目标：

+ 掌握利用GitHub进行协同开发
+ 掌握Web爬虫的基本流程
+ 实现获取网站数据
+ 熟练掌握利用Python进行项目开发



***



## 一、网络爬虫概要

### 1、网络爬虫概述

> 网络爬虫（英语：web crawler），也叫网络蜘蛛（spider），是一种用来自动浏览万维网的网络机器人。其目的一般为编纂网络索引。
>
> 网络搜索引擎等站点通过爬虫软件更新自身的网站内容或其对其他网站的索引。网络爬虫可以将自己所访问的页面保存下来，以便搜索引擎事后生成索引供用户搜索。

网络爬虫始于一个被称作种子的统一资源地址（URL）列表。当网络爬虫访问这些`URL`时，它们会甄别出页面上所有的超链接，并将它们写入一张“待访列表”，即所谓爬行区域。此区域上的`URL`将会被按照一套策略循环来访问。如果爬虫在执行的过程中复制归档和保存网站上的信息，使他们可以较容易的被查看。阅读和浏览他们存储的网站上并即时更新的信息，这些被存储的网页又被称为“快照”。越大容量的网页意味着网络爬虫只能在给予的时间内下载越少部分的网页，所以要优先考虑其下载。高变化率意味着网页可能已经被更新或者被取代。一些服务器端软件生成的`URL`也使得网络爬虫很难避免检索到重复内容。

![python爬虫](https://tva1.sinaimg.cn/large/007S8ZIlly1gg2i35qxb9j30ea073tca.jpg)

简单来说，网络爬虫就是模拟“人”的行为对浏览器进行操作，发送网络请求，接收请求响应，按照一定的规则，自动地抓取互联网信息的程序。

### 2、网络搜索引擎

> 网络搜索引擎（英语：web search engine）是设计在万维网上进行搜索，意思是指自动从万维网搜集特定的信息，提供给用户进行查询的系统。

搜索结果通常会以行列式的链接展示，亦称为搜索结果页 (Search engine results page，SERP)。这些消息链接可能是连至网页、图像、影片、信息图表、文章、研究论文或其他类型的文件。 一些搜索引擎亦会在其他的数据库或目录中搜索可用数据。与依靠人工维持的网站目录不同，搜索引擎进行的实时搜索，是以网络爬虫 (web crawler)进行运行算法得出来。而没法被搜索出来的是称为深网 (deep web)。

下图是一个网络搜索引擎的简单架构。可以看出，网络爬虫是其中的一部分，一个搜索引擎往往有着N多个网络爬虫，一般来说，这里的网络爬虫都是“合法的”。

![img](https://tva1.sinaimg.cn/large/007S8ZIlly1gg2botuz93j30pq0ea0th.jpg)

### 3、网页抓取策略

爬虫的实现由以下策略组成：

+ 指定页面下载的选择策略

- 检测页面是否改变的重新访问策略
- 定义如何避免网站过度访问的约定性策略
- 如何部署分布式网络爬虫的并行策略

### 4、讨论：“你的爬虫会送你进监狱吗？”

#### 4.1 爬虫究竟是合法还是违法的

> 《刑法》第二百八十五条规定，违反规定侵入国家事务、国防建设、尖端科学技术领域的计算机信息系统的，不论情节严重与否，构成非法侵入计算机信息系统罪。
>
> 《刑法》第二百八十六条还规定，违反国家规定，对计算机信息系统功能进行删除、修改、增加、干扰，造成计算机信息系统不能正常运行，后果严重的，构成犯罪，处五年以下有期徒刑或者拘役；后果特别严重的，处五年以上有期徒刑。而违反国家规定，对计算机信息系统中存储、处理或者传输的数据和应用程序进行删除、修改、增加的操作，后果严重的，也构成犯罪，依照前款的规定处罚

> 《网络安全法》第六十四条规定，违反本法第四十四条规定，窃取或者以其他非法方式获取、非法出售或者非法向他人提供个人信息，尚不构成犯罪的，由公安机关没收违法所得，并处违法所得一倍以上十倍以下罚款，没有违法所得的，处一百万元以下罚款。

> 《反不正当竞争法》第十二条第二款中，法律会对爬虫的这种行为进行规制。
>
> 即经营者不得利用技术手段，通过影响用户选择或者其他方式，实施下列妨碍、破坏其他经营者合法提供的网络产品或者服务正常运行的行为：…（四）其他妨碍、破坏其他经营者合法提供的网络产品或者服务正常运行的行为。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gg2had2c69j31960o44qp.jpg" alt="image-20200623200650715" style="zoom: 30%;" />



各种法律法规条文中，关于对于网络爬虫的一些行为都有着相当多的规范和限制。但是，在实际的网络世界中，江湖传言，互联网上50%以上的流量都是由爬虫创造的。似乎可以说没有爬虫，就没有今天互联网的繁荣。比如今日头条、各类门户网站的新闻，甚至是哔哩哔哩等视频网站。

那是否可以说，技术无罪？



***

+ 总结一下，爬虫所带来的风险主要有：

1. 违反网站意愿，例如网站采取反爬措施后，强行突破其反爬措施；
2. 爬虫干扰了被访问网站的正常运营；
3. 爬虫抓取了受到法律保护的特定类型的数据或信息。

其中，第3类风险主要来自于通过规避反爬虫措施抓取到了互联网上未被公开的信息。

+ 爬虫开发者在使用爬虫时应注意以下事项：

1. 严格遵守网站设置的`robots`协议；
2. 在规避反爬虫措施的同时，需要优化自己的代码，避免干扰被访问网站的正常运行；
3. 在设置抓取策略时，应注意编码抓取视频、音乐等可能构成作品的数据，或者针对某些特定网站批量抓取其中的用户生成内容；
4. 在使用、传播抓取到的信息时，应审查所抓取的内容，如发现属于用户的个人信息、隐私或者他人的商业秘密的，应及时停止并删除。

#### 4.2 君子约定：robots协议 

> `robots.txt`：放在网页服务器上，告知网络蜘蛛哪些页面内容可获取或不可获取。

例子：如淘宝的`robots.txt`. 此处含义是禁止`Baiduspider`.

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gg2aful8dbj30q009ywfn.jpg" alt="image-20200623161006970" style="zoom:67%;" />

再比如，这这个京东的`robots.txt`。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gg2ajiqae9j30ps0f076f.jpg" alt="image-20200623161347582" style="zoom:67%;" />

## 二、开发环境及GitHub介绍

### 1、Python的安装及开发环境

采用`Python`语言来实现网络爬虫。

> “Life is short, you need Python!”——*Bruce Eckel*（作者*Bruce Eckel* ，著作有的《Thinking in C++》和《Thinking in Java》）
>
> 人生苦短，我用python！

推荐使用`Anaconda`作为`python`的包管理器和环境管理器，使用 `Jupyter notebook`作为日常数据分析的工具。

本教程使用`PyCharm` 作为项目的集成开发环境，`PyCharm` 是由 JetBrains 打造的一款 Python IDE，支持 macOS、 Windows、 Linux 系统。学生可使用`cau.edu.cn` 的邮箱获取一年的免费使用权。

> `Jupyter Notebook `（前身是IPython Notebook）是一个基于Web的交互式计算环境，用于创建`Jupyter Notebook`文档。`Notebook`一词可以通俗地引用许多不同的实体，主要是`Jupyter Web`应用程序、`Jupyter Python Web`服务器或`Jupyter`文档格式（取决于上下文）。`Jupyter Notebook`文档是一个[JSON](https://zh.wikipedia.org/wiki/JSON)文档，遵循版本化模式，包含一个有序的输入/输出单元格列表，这些单元格可以包含代码、文本（使用[Markdown](https://zh.wikipedia.org/wiki/Markdown)语言）、数学、图表和富媒体，通常以`“.ipynb”`结尾扩展。

在Windows与Mac系统下，python和pycharm的的环境配置略有不同，但都属于基础操作，这里不赘述。

> python的安装及配置教程地址：https://www.runoob.com/python/python-install.html
>
> pycharm的下载地址：https://www.jetbrains.com/pycharm/
>
> PyCharm的安装教程地址：[http://www.runoob.com/w3cnote/pycharm-windows-install.html](https://www.runoob.com/w3cnote/pycharm-windows-install.html)
>
> Anaconda下载地址：https://www.anaconda.com/
>
> Jupyter Notebook介绍、安装及使用教程地址://www.jianshu.com/p/91365f343585

### 2、GitHub使用

>GitHub是通过Git进行版本控制的软件源代码托管服务平台，由GitHub公司的开发者Chris Wanstrath、PJ Hyett和Tom Preston-Werner使用Ruby on Rails编写而成。 GitHub同时提供付费账户和免费账户。

#### 3.1 git介绍

> git是一个分布式版本控制软件，最初由林纳斯·托瓦兹创作，于2005年以GPL发布。最初目的是为更好地管理Linux内核开发而设计。
>
> git最初的开发动力来自于BitKeeper和Monotone。git最初只是作为一个可以被其他前端包装的后端而开发的，但后来git内核已经成熟到可以独立地用作版本控制。很多著名的软件都使用git进行版本控制，其中包括Linux内核、X.Org服务器和OLPC内核等项目的开发流程。

####  3.2 使用GitHub环境准备

+ git与GitHub

> git是一个版本控制工具
> github是一个用git做版本控制的项目托管平台

+ 注册 GitHub 账号

进入 [GitHub ⽹站](https://github.com/) 注册⼀个⾃⼰的账户

`https://github.com/your-account` 就是你 Github 的首页。你所有的文档、代码及其历史都保存在其中的`Repositories`（仓库）中。

+ 安装 git 管理⼯具

从 [git 工具官⽹](https://git-scm.com/downloads) 直接下载安装程序，按提示选择合适系统安装。

+ 新建GitHub账户

按照GitHub系统提示进行操作，注册用户。

记住用户名密码。

+ 在pycharm中配置

需要在pycharm中配置git、GitHub相关信息。

> 配置参考：
>
> PyCharm 配置 Git 教程地址：https://cloud.tencent.com/developer/article/1478265

#### 3.2 GitHub使用

在GitHub新建一个`Repositories`（仓库），然后在pycharm中clone这个项目。之后就可以在本地的开发环境中开始coding了。

登录GitHub网站后，在右上角点击【+】，选择【New Repositories】即可。按照提示操作，输入项目名称。



![image-20200622195710573](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1bdmz2ajj31ls0l078e.jpg)



新建好`Repositories`后，回到pycharm，在【VCS】-【checkout from version control】中clone这个项目。



![image-20200622195749045](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1beaz0gqj31mi0pa4oq.jpg)

+ 本次课程将通过GitHub完成，包括组内协同开发、小组成果提交等！

> 参考材料：
>
> >  PyCharm 配置 Git 教程: https://cloud.tencent.com/developer/article/1478265
> >
> > git及GitHub教程：https://www.liaoxuefeng.com/wiki/896043488029600/900937935629664

## 三、目标网站分析

### 1、获取数据任务

获取2020年全国各地农业机械的补贴数据。按照不同的城市分别存储。

### 2、目标网站

农机360网-购置补贴查询系统。

> http://butie.nongji360.com/

![image-20200622152401522](https://tva1.sinaimg.cn/large/007S8ZIlly1gg13hg67bmj318v0u0wu6.jpg)

### 3、网站分析

对于任何一个软件项目，在开始coding之前，我们都要思考，所开发的软件系统的需求是什么，要达到什么目的。同样，在编写爬虫之前，我们需要先思考爬虫需要干什么、目标网站有什么特点，以及根据目标网站的数据量和数据特点选择合适的架构。

#### 3.1 网页分析利器-开发者工具

推荐使用Chrome的开发者工具来观察网页结构。在OS X上，通过`option+command+i`可以打开Chrome的开发者工具，或者通过**视图** -**开发者** 进入开发者模式。在Windows和Linux，对应的快捷键是"F12"。

![image-20200622195628761](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1bcwt83hj31jg0tqqrl.jpg)

#### 3.2 目标网页分析

在浏览器打开http://butie.nongji360.com/ 页面，可以看到网页中间就是我们所需要的数据。打开【开发者工具】。通过观察者页面的内容 ，我们可以发现，可以看到这个表格的标签是 `<table>`，而且整个页面只有这一个标签，即没有第二个 `<table>`标签了  。因此，在获取数据的时候，我们只需要这个`<table>` 标签下的内容。

![image-20200620231547393](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1436dit0j31850u0dp8.jpg)

#### 3.3 分析表格内的数据

针对表格内的每一行数据进行分析，可以看到，每一行的标签是`<tr>` ，每个单元格的标签是`<td>` 。

![image-20200620232013335](https://tva1.sinaimg.cn/large/007S8ZIlly1gg143tvciuj31le0s0wlp.jpg)

但是最后一个单元格的内容是【查看详情】，点击进去后，还会跳转到另一个页面，内容如下图。这时候我们发现，之前表格中的数据，在这个详情里面都有。那就是我们只获取这个详情表格中的数据就行。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gg157mtvt8j30y10u0tei.jpg" alt="image-20200622162348325" style="zoom:50%;" />

#### 3.4 表格的分页分析

下一步我们针对**分页** 进行分析。我们可以看到，分页内容全都在一个`<id_page_def>` 标签下，每一页都是一个`<a>` 标签，而尾页是在最后一个`<a>` 内。所以，我们可以通过这两个标签获取到所有的分页。

![image-20200620232501962](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1440sdu3j31hu0u07d7.jpg)



#### 3.5 分析不同城市的数据

截止目前，我们具备了获取针对某个城市的所有补贴数据的信息。那么，对于不同的城市如何处理？现在我们针对不同的城市进行分析。我们可以看到，在页面上有一个选择城市的选项。

通过开发者工具，我可以看到，城市的选择都是在一个`<tiaojian_list>` 的标签下，每个城市都有一个`<a>` 标签，`<a>` 标签内有一个链接，`text`内容是这个城市的名字。因此，我们可以通过这两个标签，获取到所有的城市。同时，通过观察可以看到，这里`<a>`标签内的链接，恰好就是对应到这个城市的URL。

![image-20200620233314109](https://tva1.sinaimg.cn/large/007S8ZIlly1gg1445lidvj31qk0u0jzv.jpg)

我们已经完成了网页内容的大概分析，对如何进行获取数据也有了基本的思路。

## 四、爬虫的代码实现

### 1、工具包

```python
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
```

> **Requests**  是用Python语言编写，基于 `urllib`，采用 `Apache2 Licensed` 开源协议的 HTTP 库。它比 `urllib`  更加方便，可以节约我们大量的工作，完全满足 HTTP 测试需求。Requests 的哲学是以 PEP 20 的习语为中心开发的，所以它比 `urllib` 更加 `Pythoner`。更重要的一点是它支持 Python3 哦！

> **Beautiful Soup** 是一个可以从 HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航，查找，修改文档的方式。**Beautiful Soup** 会帮你节省数小时甚至数天的工作时间。

### 2、下载网页源代码

第一步 ，我们先下载目标网页的源代码，使用的库是`requests`库。

```python
def downloadPage(url):
    # 下载页面方法，用requests模块，使用代理，避免重复请求次数过多；多开几个进程，加快下载速度
    headers = {
        'Connection': 'close',
        'Content-Type':'text/html; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36' }
    try:
        data = requests.get(url, headers=headers).text
        return data
    except BaseException:

        if(url in errordic):
            errordic[url] = errordic[url]+1
        else:
            errordic[url] =1
        if(errordic[url]<4):
            print(url + '【第】'+str(errordic[url])+'次重试】')
            return downloadPage(url)
        else:
            print(url + '【下载页面失败】')
            return ''
```

这里我们用的URL是某一个城市的页面地址，http://butie.nongji360.com/index/index/beijing。 

为避免访问次数过多，我们使用 `User-Agent`，中文名为用户代理，简称 UA。它是一个特殊字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等。网站可以通判断 UA 来给不同的操作系统、不同的浏览器发送不同的页面，对于爬虫来说，UA就是标明身份的第一层标识。

通过 `downloadPage`函数，我可以获取到网页的源代码，如果把它打印出来，其结果如下：

![image-20200622172135283](https://tva1.sinaimg.cn/large/007S8ZIlly1gg16vqkm0mj31ck0ra10n.jpg)

### 3、获取目标表格中的数据

这一步，我们要获取目标表格中的数据，使用的库是`BeautifulSoup`。

>**Beautiful Soup**是一个Beautiful Soup是一个Python包，功能包括解析HTML、XML文档、修复含有未闭合标签等错误的文档（此种文档常被称为tag soup）。这个扩展包为待解析的页面创建一棵树，以便提取其中的数据，这在网络数据采集时非常有用。

```python
def getData(url):
    # 获取表格中的数据，找到有用的几个信息，产品名称、公司名称、补贴
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find('table').findAll('tr')
    pageDatas = []
    for i in list:
        tds = i.findAll('td')
        if (len(tds) == 0):
            continue
        if (len(tds)<5):
            continue
        name =  tds[4].get_text()
        detailUrl = ''
        if(name == '查看详情'):
            detailUrl = tds[4].find('a').attrs['href']
        else:
            detailUrl = tds[5].find('a').attrs['href']
        res = getDetail(baseUrl+detailUrl)
        pageDatas.append(res)
    return pageDatas
```

```python
def getDetail(url):
# 获取表格中【查看详情的页面】
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    trs = soup.find("div",attrs={"class": "xiang_qing"}).find("table").findAll("tr")
    res = {}
    for tr in trs:
        tds = tr.findAll("td")
        res[tds[0].get_text()] = tds[1].get_text()
    return res
```

通过我们之前对网页的分析可以看出，表格的内容都在`<table>`标签下，而且整个源代码只有一个`<table>`标签。具体某一个单元格的数据可以通过`<tr>`和`<td>`这两个标签获取。我们的目标数据都在【查看详情】，然后再调用

通过 `getData`函数，我可以获取到某个网页的表格数据，如果把它打印出来，其结果如下：

![image-20200622172611967](https://tva1.sinaimg.cn/large/007S8ZIlly1gg170jc548j31qi0gk77i.jpg)

### 4、获取表格的全部分页

在获取表格的数据的时候，我们发现，当前页面仅显示一部分的数据，要获取到所有分页的数据，仍需要知道有多少页数据，并且找到每页数据与对应的URL之间的规律。

```python
def getPageSize(url):
    # 获取表格的分页总数
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find('div', attrs={"id": "id_page_def"}).findAll("a")
    pageNum = int(list[-1].attrs['page'])
    return pageNum
```

通过我们之前对网页的分析可以看出，分页栏的内容都在`<id_page_def>`标签下，而且整个源代码只有一个`<id_page_def>`标签。每个页面对应一个`<a>`标签，尾页是在最后一个`<a>`标签中。

通过`getPageSize`函数，我们获取到了某一个页面中，表格的所有页码，也就是表格对应的尾页是多少。

### 5、获取城市列表

这一步，我们要获取所有城市的数据，并且找到每个城市的数据与对应的URL之间的规律。这样，我们就可以获取到全国的农机购置补贴的数据了。

```python
def getCityList(url):
    # 获取所有的城市信息列表
    cityList = []
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find("div", attrs={"class": "tiaojian_list"}).findAll('a')
    for a in list:
        name = a.get_text()
        href = a.attrs['href']
        cityList.append({'href': href, 'name': name})
    return cityList
```

通过我们之前对网页的分析可以看出，城市数据内容都在`<tiaojian_list>`标签下，而且整个源代码只有一个`<tiaojian_list>`标签。每个城市的数据对应一个`<a>`标签。

通过`getCityList`函数，我们获取到了这个网站中所有的城市数据。如果把这个函数的内容打印出来，结果如下：

![image-20200622175709003](https://tva1.sinaimg.cn/large/007S8ZIlly1gg17wqswusj31oo0ic77e.jpg)

### 6、获取全部城市的目标数据

这是最后一步，我们通过之前的函数，已经实现下载网页源代码、获取表格中的数据、获取表格的分页数、获取全部城市的信息。现在，我们就要实现一次性获取全部城市的购置补贴数据。

```python
def downAllDatas():
    # 下载所有城市的数据
    url = "http://butie.nongji360.com/index/index/beijing"
    citylist = getCityList(url)
    datasThreads = []
    with ThreadPoolExecutor(max_workers=40) as t:
      for city in citylist:
          d= t.submit(getCityData, city)
          datasThreads.append(d)
      for future in as_completed(datasThreads):
          print(future)

def getCityData(city):
    # 下载每个城市的数据，并写入JSON
    datas = {}
    cityHref = baseUrl + city.get('href')
    cityData = []
    pageSize = getPageSize(cityHref)
    print(city.get('name') + ":[总页数]" + str(pageSize))

    for i in range(pageSize):
        print(city.get('name') + ":[当前页数]" + str(i+1))
        durl = cityHref + "?p=" + str(i + 1)
        pageDatas = getData(durl)
        cityData.extend(pageDatas)
    datas[city.get('name')] = cityData
    with open(city.get('name')+'.json', 'w', encoding="utf-8") as f:
        print('写入文件'+city.get('name')+'.json')
        json.dump(datas, f, ensure_ascii=False)
    return 'success'
```

截止目前，我们就完成了农机购置补贴数据的获取，获取结果我们存在JSON中，打印出来可以看到如下结果。



![image-20200622174149289](https://tva1.sinaimg.cn/large/007S8ZIlly1gg17guztcuj31hc0oejwr.jpg)

## 五、总结

+ 介绍了网络爬虫的概要
+ 介绍了使用到的开发环境和工具
+ 分析了目标网站并找到抓取策略
+ 实现了全国农机购置补贴数据的抓取



## 六、拓展

### 1、数据库的使用

> Python 操作 MySQL 数据库教程地址：https://www.runoob.com/python/python-mysql.html

### 2、数据可视化-Echarts

ECharts 是一个使用 JavaScript 实现的开源可视化库，涵盖各行业图表，满足各种需求。

ECharts 遵循 Apache-2.0 开源协议，免费商用。

ECharts 兼容当前绝大部分浏览器（IE8/9/10/11，Chrome，Firefox，Safari等）及兼容多种设备，可随时随地任性展示。

> Echarts官方网站地址：https://echarts.apache.org/zh/index.html
>
> Echarts官方教程地址 ：https://echarts.apache.org/zh/tutorial.html

![image-20200623212257535](https://tva1.sinaimg.cn/large/007S8ZIlly1gg2jh7o2k7j31nz0u04qt.jpg)

## 七、实训内容及要求

### 1、 大作业

项目名称：题目可参考附录，或者自拟题目（需向助教确认）。

完成方式：

+ 分组完成，组长负责协调组内分工，每个人需要有明确的任务。
+ 使用GitHub进行协同开发，每个组一个`Repositories`（仓库），建好`Repositories`后将链接发给助教。
+ 每组除了完成自己的项目之外，还需要在本地运行其余各组的代码（在该组宣布完成或者到时间节点后 ），并在GitHub提交运行报告。
+ 结课汇报时，小组根据视频内容进行汇报，每人个均都需要发言，汇报时间5-10分钟。

提交成果：

+ GitHub的`Repositories`（仓库）地址。
+ 成果汇报的视频，时长5～10分钟。介绍项目情况、组员贡献、实现过程等。

### 2、小作业

作业要求

+ 利用Windows的IIS等服务器建立个人网站，以个人简介为主要内容。

完成方式

+ 个人完成。

作业成果

+ 提交视频介绍，不超过2分钟。

+ GitHub的`Repositories`（仓库）地址（可选）。

### 3、成绩组成

#### 3.1 大作业

分数占比：60%。

打分说明：根据提交的作业成果打分。组内成员的分数由组长打分，最高分不高于小组的分数，每位组员的分值不可以全部一致。（如：给A组的打分为90分，组长可给每个组员打分的最高值为90分。）

#### 3.2 小作业

分数占比：20%。

打分说明：根据提交的作业成果进行打分。

#### 3.3 小组互评

分数占比：20%。

打分说明：小组间互相打分，分数百分制，分数标注在对应小组的代码运行报告封面。

### 附录：

+ 全国农产品批发市场价格信息系统：http://pfsc.agri.cn/
+ 全国农机化信息服务平台：http://www.njztc.com/