# -*- coding=utf8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xlwt


star_url = 'https://hotel.meituan.com/beijing/'

# 通过selenium模拟服务器获取element解析每页的信息
# 1.

def get_each_url(url):

    chrome_options = Options()
    chrome_options.add_argument('headless')  # 设置静默浏览模式
    chrome_options.add_argument('disable-gpu')  # 禁止GPU硬件加速
    driver = webdriver.Chrome(executable_path=r'C:\Users\M\anaconda3\chromedriver.exe')
    driver.get(url)
    # print(driver.page_source)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    page_info = soup.find_all('li', class_='page-link')  # 获取酒店首页的页面导航条信息
    page_num = page_info[-1].find('a').get_text()  # 获取酒店页面的总页数
    print(page_num)
    # return int(page_num)   # 返回酒店页面的总页数


    # hotel_info = {}
    hotel_id = ['酒店名', '网址', '酒店地址', '评价']
    col_num = 1
    page_num = 1

    # book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建excel文件
    # sheet = book.add_sheet('hotel_info', cell_overwrite_ok=True)  # 创建excel sheet表单
    #
    # for i in range(len(hotel_id)):  # 写入表单第一行，即列名称
    #     sheet.write(0, i, hotel_id[i])  # excel中写入第一行列名


    for item in driver.find_elements_by_class_name('info-wrapper'):
        print(item)
        hotel_info = item.find_element_by_class_name('poi-title').text
        print(hotel_info)
        # hotel_info['link'] = item.find_element_by_class_name('poi-title').get_attribute('href')
        # hotel_info['address'] = item.find_element_by_class_name('poi-address').text.split(' ')[1]
        # hotel_info['star'] = item.find_element_by_class_name('poi-grade').text
        # print(hotel_info)
    # # 将当前页面中的酒店信息获取到后，写入excel的行中
    # for i in range(len(hotel_info.values())):
    #     sheet.write(col_num, i, list(hotel_info.values())[i])
    # col_num += 1
    #
    # # driver.find_element_by_class_name('paginator').find_element_by_class_name('next').find_element_by_tag_name(
    # #     'a').click()  # 一个页面写完后，通过点击"下一页"图标至下一页，继续获取
    # # page_num += 1
    # book.save('./hotel_info_huangshan.csv')


get_each_url(star_url)

