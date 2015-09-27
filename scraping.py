# coding= utf-8
from selenium import webdriver
import time

path = '/Users/Peterkwok/Downloads/phantomjs'
driver = webdriver.PhantomJS(path)
driver.get('http://flight.qunar.com')

route = driver.find_element_by_class_name('crl_sp_city')
departure = route.find_elements_by_xpath('div')[0]
arrival = route.find_elements_by_xpath('div')[1]

text_area = departure.find_element_by_xpath('div/input')
text_area.click()
text_area.send_keys('beijing')
time.sleep(2)
suggest_area = departure.find_element_by_class_name('q-suggest')
suggest_cities = suggest_area.find_elements_by_xpath('table/tbody/tr')
print 'Selected City : ' + suggest_cities[0].text
suggest_cities[0].click()

text_area = arrival.find_element_by_xpath('div/input')
text_area.click()
text_area.send_keys('hangzhou')
time.sleep(2)
suggest_area = arrival.find_element_by_class_name('q-suggest')
suggest_cities = suggest_area.find_elements_by_xpath('table/tbody/tr')
print u'Selected City : ' + suggest_cities[0].text
suggest_cities[0].click()

date = driver.find_element_by_class_name('crl_sp_date')
text_area = date.find_element_by_id('fromDate')
text_area.click()
text_area.clear()
text_area.send_keys('2015-10-7')

button = driver.find_element_by_class_name('btn_search')
button.click()
time.sleep(2)

f = open('result.html', 'w')
f.write(driver.page_source.encode('utf-8'))
f.close()
driver.quit()