# coding= utf-8
from selenium import webdriver
import time

path = '/Users/Peterkwok/Downloads/phantomjs-1.9.7-macosx/bin/phantomjs'
driver = webdriver.PhantomJS(path)
driver.get('http://flight.qunar.com')
time.sleep(2)

from_city = driver.find_elements_by_xpath('//form[@id=\'dfsForm\']/div[@class=\'crl_sp_city\']/div')[0]
input_area = driver.find_element_by_name('fromCity')
input_area.click()
input_area.clear()
input_area.send_keys('beijing')
time.sleep(2)
print input_area.text
suggest_area = from_city.find_elements_by_xpath('//div[@class=\'q-suggest\']/table/tbody/tr')[0]
print 'suggest: ', suggest_area.text
suggest_area.click()

to_city = driver.find_elements_by_xpath('//form[@id=\'dfsForm\']/div[@class=\'crl_sp_city\']/div')[1]
input_area = to_city.find_element_by_name('toCity')
input_area.click()
input_area.clear()
input_area.send_keys('zhengzhou')
time.sleep(2)
print input_area.text
suggest_area = to_city.find_elements_by_xpath('//div[@class=\'q-suggest\']/table/tbody/tr')[0]
print 'suggest: ', suggest_area.text
suggest_area.click()

f = open('result.html', 'w')
f.write(driver.page_source.encode('utf-8'))
f.close()
driver.quit()
