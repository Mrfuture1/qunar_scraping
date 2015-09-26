# coding= utf-8
from selenium import webdriver
import time

path = '/Users/Peterkwok/Downloads/phantomjs-1.9.7-macosx/bin/phantomjs'
driver = webdriver.PhantomJS(path)
driver.get('http://flight.qunar.com')
from_city = driver.find_element_by_name('fromCity')
from_city.send_keys('beijing')
to_city = driver.find_element_by_name('toCity')
to_city.send_keys('zhengzhou')
from_date = driver.find_element_by_name('fromDate')
from_date.send_keys('2015-10-1')
button = driver.find_elements_by_class_name('btn_search')[0]
button.click()
time.sleep(20)
f = open('result.html', 'w')
f.write(driver.page_source.encode('utf-8'))
driver.close()
