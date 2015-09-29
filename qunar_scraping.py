# -*- coding: UTF-8 -*-
from selenium import webdriver
import time
import content_parse


class Scraping(object):
    # 初始化爬虫：设置出发地、目的地、出发时间
    def __init__(self, departure, arrival, date):
        path = '/Users/Peterkwok/Downloads/phantomjs'
        self.url = 'http://flight.qunar.com'
        self.driver = webdriver.PhantomJS(path)

        self.departure = departure
        self.arrival = arrival
        self.date = date

    # 向网页添加数据
    def insert_info(self):
        self.driver.get(self.url)
        route = self.driver.find_element_by_class_name('crl_sp_city')
        departure = route.find_elements_by_xpath('div')[0]
        arrival = route.find_elements_by_xpath('div')[1]
        date = self.driver.find_element_by_class_name('crl_sp_date')

        self.insert_departure(departure)
        self.insert_arrival(arrival)
        self.insert_date(date)

    # 添加出发地
    def insert_departure(self, departure):
        text_area = departure.find_element_by_xpath('div/input')
        text_area.click()
        text_area.send_keys(self.departure)
        time.sleep(2)
        suggest_area = departure.find_element_by_class_name('q-suggest')
        suggest_cities = suggest_area.find_elements_by_xpath('table/tbody/tr')
        print 'Selected City : ' + suggest_cities[0].text
        suggest_cities[0].click()

    # 添加目的地
    def insert_arrival(self, arrival):
        text_area = arrival.find_element_by_xpath('div/input')
        text_area.click()
        text_area.send_keys(self.arrival)
        time.sleep(2)
        suggest_area = arrival.find_element_by_class_name('q-suggest')
        suggest_cities = suggest_area.find_elements_by_xpath('table/tbody/tr')
        print u'Selected City : ' + suggest_cities[0].text
        suggest_cities[0].click()

    # 添加出发时间
    def insert_date(self, date):
        text_area = date.find_element_by_id('fromDate')
        text_area.click()
        text_area.clear()
        text_area.send_keys(self.date)

    # 执行查询
    def execute_query(self):
        button = self.driver.find_element_by_class_name('btn_search')
        button.click()
        time.sleep(2)

    # 滚动页面完成页面的动态加载
    def scroll_page(self):
        flight_subscribe = self.driver.find_element_by_class_name('subenv')
        for x in xrange(5):
            self.driver.execute_script("return arguments[0].scrollIntoView();", flight_subscribe)
            time.sleep(1)

    # 存储结果页面
    def page_store(self):
        self.scroll_page()
        print 'store the ' + str(1) + ' page'
        with open('result_1.html', 'w') as f:
            f.write(self.driver.page_source.encode('utf-8'))
            f.close()
        page_turning = self.driver.find_element_by_id('detailPage')
        if page_turning.is_displayed():
            pages = page_turning.find_elements_by_xpath('div[@id=\'hdivPager\']/a')
            for x in xrange(len(pages) - 1):
                pages[-1].click()
                self.scroll_page()
                print 'store the ' + str(x + 2) + ' page ...'
                with open('result_' + str(x + 2) + '.html', 'w') as f:
                    f.write(self.driver.page_source.encode('utf-8'))
                    f.close()
            return len(pages)
        return 1

    # 进行页面解析
    def page_parse(self, n):
        for x in xrange(1, n + 1):
            print 'parse the ' + str(x) + ' page ...'
            file_name = 'result_' + str(x) + '.html'
            content_parse.parse_content(file_name)

    def destory_driver(self):
        self.driver.quit()

    # 爬虫执行流程
    def qunar_scraping(self):
        print 'opening the page :' + self.url + '...'
        print 'now input your data ...'
        self.insert_info()
        print 'you are from ' + self.departure + ' and going to ' + self.arrival + ' at ' + self.date
        print 'execute querying ...'
        self.execute_query()
        print 'begin to store the pages ...'
        page_num = self.page_store()
        print 'now you get ' + str(page_num) + ' pages ...'
        print 'start to parse the pages ...'
        self.page_parse(page_num)
        print 'all done!'
        self.destory_driver()


# 进行测试
if __name__ == '__main__':
    departure = 'beijing'
    arrival = 'zhengzhou'
    date = '2015-10-7'
    s = Scraping(departure, arrival, date)
    s.qunar_scraping()
