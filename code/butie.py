#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 常量定义

# 定义基础URL，即目标url
baseUrl = "http://butie.nongji360.com"
#定义错误字典
errordic = {}


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


def getData(url):
    # 获取表格中的数据
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
    print(pageDatas)
    return pageDatas


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

def getPageSize(url):
    # 获取表格的分页总数
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find('div', attrs={"id": "id_page_def"}).findAll("a")
    pageNum = int(list[-1].attrs['page'])
    return pageNum


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
    print(cityList)
    return cityList


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


if __name__ == '__main__':
    # url = 'http://butie.nongji360.com/index/index/beijing'
    # getCityList(url)
    downAllDatas()