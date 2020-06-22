#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import json

# 常量定义
datas = {}
# 定义输出结果
baseUrl = "http://butie.nongji360.com"
# 定义查询的基础URL
filename = 'loadjson.json'
# 定义输出文件


def downloadPage(url):
    # 下载页面方法，用requests模块，使用代理，避免重复请求次数过多
    headers = {
        'Content-Type':'text/html; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36' }
    data = requests.get(url, headers=headers).text
    return data


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


def getPageSize(url):
    # 获取表格的分页总数
    content = downloadPage(url)
    soup = BeautifulSoup(content, 'html.parser')
    list = soup.find('div', attrs={"id":"id_page_def"}).findAll("a")
    return int(list[-1].attrs['page'])


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


def downAllDatas():
    # 下载所有城市的数据
    url = "http://butie.nongji360.com/catalog/index/anhui"
    citylist = getCityList(url)
    for city in citylist:
        cityHref = baseUrl+city.get('href')
        cityData = []
        pageSize = getPageSize(cityHref)
        for i in range(pageSize):
            pageDatas = getData(cityHref + "?p" + str(i))
            cityData.extend(pageDatas)
        # i = 1
        # while(i < pageSize):
        #     pageDatas = getData(cityHref+"?p"+str(i))
        #     cityData.extend(pageDatas)
        #     i += i
        datas[city.get('name')] = cityData
    print(datas)
    return datas


if __name__ == '__main__':
    url = "http://butie.nongji360.com/catalog/index/anhui"
    #getCityList(url)
    downAllDatas()
    with open('datacatalog.json', 'w',encoding="utf-8") as f:
        json.dump(datas, f, ensure_ascii=False)