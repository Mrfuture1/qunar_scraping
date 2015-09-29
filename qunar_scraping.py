# -*- coding: UTF-8 -*-
from selenium import webdriver
import time
import content_parse


class Scraping(object):
    def __init__(self, departure, arrival, date):
        path = '/Users/Peterkwok/Downloads/phantomjs'
        self.url = 'http://flight.qunar.com'
        self.driver = webdriver.PhantomJS(path)

        self.departure = departure
        self.arrival = arrival
        self.date = date

    def insert_info(self):
        self.driver.get(self.url)
        route = self.driver.find_element_by_class_name('crl_sp_city')
        departure = route.find_elements_by_xpath('div')[0]
        arrival = route.find_elements_by_xpath('div')[1]
        date = self.driver.find_element_by_class_name('crl_sp_date')

        self.insert_departure(departure)
        self.insert_arrival(arrival)
        self.insert_date(date)

    def insert_departure(self, departure):
        text_area = departure.find_element_by_xpath('div/input')
        text_area.click()
        text_area.send_keys(self.departure)
        time.sleep(2)
        suggest_area = departure.find_element_by_class_name('q-suggest')
        suggest_cities = suggest_area.find_elements_by_xpath('table/tbody/tr')
        print 'Selected City : ' + suggest_cities[0].text
        suggest_cities[0].click()

    def insert_arrival(self, arrival):
        text_area = arrival.find_element_by_xpath('div/input')
        text_area.click()
        text_area.send_keys(self.arrival)
        time.sleep(2)
        suggest_area = arrival.find_element_by_class_name('q-suggest')
        suggest_cities = suggest_area.find_elements_by_xpath('table/tbody/tr')
        print u'Selected City : ' + suggest_cities[0].text
        suggest_cities[0].click()

    def insert_date(self, date):
        text_area = date.find_element_by_id('fromDate')
        text_area.click()
        text_area.clear()
        text_area.send_keys(self.date)

    def execute_query(self):
        button = self.driver.find_element_by_class_name('btn_search')
        button.click()
        time.sleep(2)

    def scroll_page(self):
        flight_subscribe = self.driver.find_element_by_class_name('subenv')
        for x in xrange(5):
            self.driver.execute_script("return arguments[0].scrollIntoView();", flight_subscribe)
            time.sleep(1)

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
                print 'store the ' + str(x + 2) + ' page'
                with open('result_' + str(x + 2) + '.html', 'w') as f:
                    f.write(self.driver.page_source.encode('utf-8'))
                    f.close()
            return len(pages)
        return 1

    def page_parse(self, n):
        for x in xrange(1, n + 1):
            file_name = 'result_' + str(x) + '.html'
            content_parse.parse_content(file_name)

    def destory_driver(self):
        self.driver.quit()

    def qunar_scraping(self):
        self.insert_info()
        self.execute_query()
        page_num = self.page_store()
        self.page_parse(page_num)
        self.destory_driver()


if __name__ == '__main__':
    departure = 'beijing'
    arrival = 'zhengzhou'
    date = '2015-10-7'
    s = Scraping(departure, arrival, date)
    s.qunar_scraping()
