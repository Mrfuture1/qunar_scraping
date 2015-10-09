# -*- coding: UTF-8 -*-
# 苏宁与京东相似，价格也是异步取得
# 经过分析：取得价格的url为 http://ds.suning.cn/ds/prices/000000000 + id + -9017--1-SES.product.priceCenterCallBack.jsonp
# 其中id为商品详情页面的中包含的特定位数的数字
import requests
from bs4 import BeautifulSoup
import re


def get_next(response):
    tree = BeautifulSoup(response, 'lxml')
    next_page = tree.find('a', id='nextPage')['href']
    next_url = 'http://list.suning.com' + next_page
    return next_url


def get_price(id):
    price_url = 'http://ds.suning.cn/ds/prices/000000000' + id + '-9017--1-SES.product.priceCenterCallBack.jsonp'
    price_json = requests.get(price_url).content
    return re.match(r'.*?\"price\":\"(.*?)\".*', price_json).group(1)


def page_parsing(response):
    f = open('result.txt', 'a')
    tree = BeautifulSoup(response, 'lxml')
    titles = tree.find_all('div', class_='i-name limit clearfix')
    for title in titles:
        title_content = title.text.strip()

        link = title.a['href']
        id = re.match(r'.*?/(\d+)\.html', link).group(1)
        price = get_price(id)

        detail = tree.find('div', class_='i-stock limit clearfix')
        has_stock = detail.span.text
        res_num = detail.a.text.strip()
        result = title_content + '  ' + price + '  ' + has_stock + '  ' + res_num + '\n'
        f.write(result.encode('utf-8'))
    f.close()


def suning_scraping(url):
    page = requests.get(url).content
    page_parsing(page)
    return get_next(page)


url = 'http://list.suning.com/0-20006-0-0-0-9017.html'
for x in xrange(10):
    print 'Requesting the ' + str(x + 1) + ' page: ' + url
    url = suning_scraping(url)
