# -*- coding: UTF-8 -*-
# 使用爬虫直接访问 http://www.bilibili.com/video/douga-else-1.html 时获取的网页并没有内容
# 经过分析后发现浏览器请求 http://www.bilibili.com/list/default-27-1-2015-10-04~2015-10-11.html 这样的链接后将内容整体添加到页面之上
import requests
import time
import Queue
from bs4 import BeautifulSoup
import threading


def url_generate(n):
    start_date = time.localtime(time.time() - 60 * 60 * 24 * 7)
    url = 'http://www.bilibili.com/list/default-27-' + str(n) + '-' + time.strftime("%Y-%m-%d", start_date) + '~' + \
          time.strftime("%Y-%m-%d", time.localtime()) + '.html'
    return url


def get_page(q):
    for x in xrange(10):
        url = url_generate(x + 1)
        q.put(requests.get(url).content)


def parse_page(q):
    for x in xrange(10):
        page = q.get(True)
        tree = BeautifulSoup(page, 'lxml')
        items = tree.find_all('div', class_='l-item')
        result = []
        for item in items:
            title = item.find('div', class_='info').text
            view = item.find('i', class_='gk').text
            store = item.find('i', class_='sc').text
            barrage = item.find('i', class_='dm').text
            user_name = item.find('i', class_='up r10000').text
            date = item.find('i', class_='date').text
            res = user_name + u'  ' + date + u'\n' + view + u'  ' + store \
                  + u'  ' + barrage + u'\n' + title + u'\n'
            result.append(res.encode('utf-8'))
        with open('result.txt', 'a') as f:
            f.write('\n'.join(result) + '\n')
            f.close()


def multithread_scraping():
    queue = Queue.Queue()
    t1 = threading.Thread(target=get_page, args=(queue,))
    t2 = threading.Thread(target=parse_page, args=(queue,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    multithread_scraping()
