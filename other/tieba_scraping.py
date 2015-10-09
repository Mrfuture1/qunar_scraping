# -*- coding: UTF-8 -*-
import urllib
from bs4 import BeautifulSoup
import re

data = urllib.quote('火影忍者')
url = 'http://tieba.baidu.com/f?ie=utf-8&kw=' + data
response = urllib.urlopen(url).read()
with open('page_1.html', 'w') as f:
    f.write(response)
    f.close()
for x in range(5):
    dom = BeautifulSoup(response, 'lxml')
    next_page = dom.find('a', class_='next pagination-item ')
    url = next_page['href']
    response = urllib.urlopen(url).read()
    with open('page_' + str(x + 2) + '.html', 'w') as f:
        f.write(response)
    f.close()

result = open('result.txt', 'w')
for x in xrange(6):
    f = open('page_' + str(x + 1) + '.html', 'r').read()
    page = BeautifulSoup(f, 'lxml')
    contents = page.find_all('li', class_=' j_thread_list clearfix')
    for content in contents:
        author = content.find('div', class_='threadlist_author pull_right').span['title']
        name = re.match(r'.*? (.*)', author).group(1)
        title = content.div.a.text
        detail = content.find('div', class_='threadlist_abs threadlist_abs_onlyline ').string
        reply_num = content.find('span', 'threadlist_rep_num center_text').text
        res = name + '    ' + title + '    ' + reply_num + '\n' + detail.strip() + '\n\n'
        result.write(res.encode('utf-8'))
result.close()
