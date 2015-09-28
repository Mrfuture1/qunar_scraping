# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('result_1.html').read().decode('utf-8'))
flight_detail = soup.find('div', 'e_fly_lst')
items = flight_detail.contents
# contents得到所有的直接子节点

per_detail = ''
for item in items:
    pass
air_name = items[-4].find_all('div', class_='a-name')
name_set = set([])
for name in air_name:
    name_set.add(name.text)
print name_set
# 获取航班名称


departure_time = items[0].find('div', class_='a-dep-time')
print departure_time.text
# 获取出发时间

departure_airport = items[0].find('div', class_='a-dep-airport')
print departure_airport.text
# 获取出发机场

during_time = items[0].find('div', class_='a-tm-be')
print during_time.text
# 获取时长

arrival_time = items[0].find('div', class_='a-arr-time')
print arrival_time.text
# 获取到达时间

arrival_airport = items[0].find('div', class_='a-arr-airport')
print arrival_airport.text
# 获取到达机场

delay_per = items[0].find_all('p', class_='a-pty-mint')
for x in delay_per:
    print x.text
# 获取时延概率及时间

price_tag = items[3].find('div', class_='a-low-prc')
price = price_tag.find_all('b')
price_list = [str(word) for word in price[0].text]
for x in xrange(1, len(price)):
    m = re.search('\'left:-(\d{2})px\'', str(price[x].attrs))
    price_list[len(price_list)-int(m.group(1))/16] = str(price[x].text)
price_final = ''.join(price_list)
print price_final
# 获取真正的价格


