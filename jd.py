#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 18:28
# @Author  : 刘晨
# @File    : jd.py
# @Software: PyCharm Community Edition

import requests
import re
from bs4 import BeautifulSoup
import xlwt

def Jd(url):

    head = {
        'User - Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML,likeGecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept - Encoding': 'gzip, deflate, br',
    }
    reg = r'<em><font class="skcolor_ljg">(.*?)</font>(.*?)</em>'
    re1 = re.compile(reg)
    try:
        r = requests.get(url, headers = head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')
        listall = []
        i=2
        a = soup.select('.p-price')
        for i in range(len(a)):
            list = []
            price = soup.select('.p-price')[i].find_all('i')[0].get_text()
            name = soup.select('.p-name')[i].find_all('em')[0].get_text()
            commit = soup.select('.p-commit')[i].find_all('strong')[0].get_text()
            src = 'https:'+soup.select('.p-img')[i].find_all('a')[0]['href']
            list.append(name)
            list.append(price)
            list.append(commit)
            list.append(src)
            listall.append(list)
        return listall

    except:
        return "产生异常"

if __name__=="__main__":
    name = input('请输入商品名称')
    count = input('请输入获取条数（30的倍数）')
    page = int(int(count)/30)
    list = []
    for i in range(page):
        page = str(i)
        url = 'https://search.jd.com/Search?keyword=' + name + '&enc=utf-8&page='+page
        a = Jd(url)
        list.append(a)

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('JD')
    head = ['商品名称', '价格', '评价数量','商品链接']  # 表头
    for h in range(len(head)):
        sheet.write(0, h, head[h])  # 写入表头
    i = 1
    for abc in list:
        for list in a:
            j = 0
            for data in list:
                sheet.write(i, j, data)
                j += 1
            i += 1
    path = 'G:\JD.xls'
    book.save(path)
    print('已存入:'+path)
