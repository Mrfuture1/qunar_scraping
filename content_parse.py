# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def parse_content(name):
    soup = BeautifulSoup(open(name).read().decode('utf-8'), 'lxml')
    flight_detail = soup.find('div', 'e_fly_lst')
    items = flight_detail.contents
    # contents得到所有的直接子节点

    with open('flight.txt', 'a') as f:
        for item in items:
            f.write(parse_item(item)+'\n')
        f.close()


def parse_item(item):
    per_detail = ''
    air_name = item.find('div', class_='a-name')
    per_detail += u'{:^8}'.format(air_name.text)
    # 获取航班名称

    departure_airport = item.find('div', class_='a-dep-airport')
    per_detail += u'{:^10}'.format(departure_airport.text)
    # 获取出发机场

    departure_time = item.find('div', class_='a-dep-time')
    per_detail += u'{:^8}'.format(departure_time.text)
    # 获取出发时间

    during_time = item.find('div', class_='a-tm-be')
    per_detail += u'{:^10}'.format(during_time.text)
    # 获取时长

    arrival_airport = item.find('div', class_='a-arr-airport')
    per_detail += u'{:^10}'.format(arrival_airport.text)
    # 获取到达机场

    arrival_time = item.find('div', class_='a-arr-time')
    per_detail += u'{:^10}'.format(arrival_time.text)
    # 获取到达时间

    delay_per = item.find_all('p', class_='a-pty-mint')
    for x in delay_per:
        per_detail += u'{:^6}'.format(x.text)
    # 获取时延概率及时间

    price_tag = item.find('div', class_='a-low-prc')
    price = price_tag.find_all('b')
    price_list = [str(word) for word in price[0].text]
    for x in xrange(1, len(price)):
        m = re.search('\'left:-(\d{2})px\'', str(price[x].attrs))
        price_list[len(price_list) - int(m.group(1)) / 16] = str(price[x].text)
    price_final = ''.join(price_list)
    per_detail += u'{:^6}'.format(price_final)
    # 获取真正的价格

    return per_detail


if __name__ == '__main__':
    parse_content(u'result_1.html')
    parse_content(u'result_2.html')
