# coding= utf-8
from selenium import webdriver
import time
import content_parse

path = '/Users/Peterkwok/Downloads/phantomjs'
driver = webdriver.PhantomJS(path)
driver.get('http://flight.qunar.com')

route = driver.find_element_by_class_name('crl_sp_city')
departure = route.find_elements_by_xpath('div')[0]
arrival = route.find_elements_by_xpath('div')[1]
date = driver.find_element_by_class_name('crl_sp_date')

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

text_area = date.find_element_by_id('fromDate')
text_area.click()
text_area.clear()
text_area.send_keys('2015-10-7')

button = driver.find_element_by_class_name('btn_search')
button.click()
time.sleep(2)

# 翻滚页面至加载完毕，两种不同的方法
flight_subscribe = driver.find_element_by_class_name('subenv')
for x in xrange(5):
    driver.execute_script("return arguments[0].scrollIntoView();", flight_subscribe)
    time.sleep(1)

# 得到所有的结果页面
print 'store the ' + str(1) + ' page'
f = open('result_1.html', 'w')
f.write(driver.page_source.encode('utf-8'))
f.close()

page_turning = driver.find_element_by_id('detailPage')
if page_turning.is_displayed():
    pages = page_turning.find_elements_by_xpath('div[@id=\'hdivPager\']/a')
    for x in xrange(len(pages) - 1):
        pages[-1].click()
        for y in xrange(5):
            driver.execute_script("return arguments[0].scrollIntoView();", flight_subscribe)
            time.sleep(1)
        print 'store the ' + str(x + 2) + ' page'
        f = open('result_' + str(x + 2) + '.html', 'w')
        f.write(driver.page_source.encode('utf-8'))
        f.close()
driver.quit()
