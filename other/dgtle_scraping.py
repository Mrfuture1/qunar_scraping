import requests
from lxml import html


# 发送请求并存储页面至文件
def request(url, file_name):
    print 'opening the page :' + url
    # 发请求 res为返回页面
    res = requests.get(url)
    # 写文件
    with open(file_name, 'wb')as f:
        print 'storing the file :' + file_name
        f.write(res.content)
        f.close()
    return res


# 获得下一页的链接
# 调用发请求函数存储下一页
def turn_page(res, n):
    # 获得页面结构
    tree = html.fromstring(res.content)
    # 获得下一页的链接
    pages_url = tree.xpath('//*[@id="ct"]/div[1]/div/div[5]/div/a')
    next_page = pages_url[-1].attrib['href']
    # 请求下一页
    return request(next_page, 'dgtle_' + str(n) + '.html')


# 解析页面
def page_parse(name):
    # 以只读方式打开文件
    content = open(name, 'r')
    # 获得html树形结构
    tree = html.parse(content)
    # 获得所有条目items
    items = tree.xpath('//*[@id="moderate"]/table/tbody')
    # 以追加写入方式打开文件
    result = open('result.txt', 'a')
    # 进行循环处理每个条目
    for item in items:
        # 获得每个条目主要内容的父节点
        page_content = item.xpath('tr/th/div')[0]
        # 定义解析后的字符串
        item_content = ''

        # 获得用户名
        user_name = page_content.xpath('p/a/span/text()')[0]
        # 将用户名添加至结果输出
        item_content += user_name + ':   '

        # 获得文章标题
        title = page_content.xpath('h2/span/a/text()')[0]
        # 将文章标题添加至输出
        item_content += title + '     '

        # 获得发布时间
        release_time = page_content.xpath('p/a/span')[1].text
        # 添加发布时间
        item_content += release_time + '   '

        # 获得回复数
        response_num = page_content.xpath('p/span/text()')[0]
        # 添加回复数
        item_content += response_num + '\n'
        # 将该条目写入已打开的文件
        result.write(item_content.encode('utf-8'))
    # 文件关闭
    result.close()


# 进行该模块的测试
if __name__ == '__main__':
    # 定义要请求的网站
    req_url = 'http://bbs.dgtle.com/forum-2-1.html'
    print 'open the page :' + req_url
    # 获得返回的页面
    response = request(req_url, 'dgtle_1.html')
    # 通过循环不断请求并存储下一页，共存储10页
    for x in range(9):
        response = turn_page(response, x + 2)
    #解析得到的所有页面
    for x in range(1, 11):
        page_name = 'dgtle_' + str(x) + '.html'
        print 'parsing the file :' + page_name
        # 页面解析
        page_parse(page_name)
