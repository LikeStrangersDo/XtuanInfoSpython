# -*- coding=utf-8 -*-
# @Time:2020-12-17 
# @Author:Malone_M
# @File：Mt_AddPhone&Coordinates.py
# @Software：PyCharm

import xlrd, xlwt
from bs4 import BeautifulSoup
import requests, re, time
import random

add_info_id = ['name', 'phone', '房间总量', '开业时间', '装修时间', '酒店简介', '坐标']
# 创建一个新的excel文件计入信息
book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建excel文件
sheet = book.add_sheet('hotel_info', cell_overwrite_ok=True)  # 创建excel sheet表单
# 写入表头
for i in range(len(add_info_id)):  # 写入表单第一行，即列名称
    sheet.write(0, i, add_info_id[i])  # excel中写入第一行


def main():

    # 1.读取hotel_info_beijing获取links列表
    excel_path = './hotel_info_beijing.xls'
    links = get_links(excel_path)
    # 2.for循环逐个request访问并获取所需要的信息
    col_num = 0
    for start_link in links:
        data = get_info(start_link)
        for x in range(len(data.values())):
            sheet.write(col_num, x, list(data.values())[x])
        x += 1
        col_num += 1
        book.save('./hotel_info_beijing_addinfo.xls')
        print('第{}行数据爬取完毕'.format(col_num))
        time.sleep(random.randint(2, 8))


def get_links(excel_path):
    """打开excel获取links"""
    book1 = xlrd.open_workbook(excel_path)
    sheet1 = book1.sheet_by_name('hotel_info')
    links = sheet1.col_values(1, start_rowx=1)
    return links


def get_info(url):
    """通过传入的链接获取电话及坐标信息"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.111 Safari/537.36"}

    try:
        res = requests.get(url, headers=headers)
    except:
          print('出错了')
    else:
        add_info = {}  # 创建一个空字典记录加入的信息内容

        # 查找内容正则表达式
        find_name = re.compile(r'"poiName":"(.*?)"')
        find_phone = re.compile(r'"酒店电话","phone":"(.*?)"')
        find_RoomsNum = re.compile(r'"attrDesc":"客房总量","attrValue":"(.*?)"')  # 输出 80
        find_OpenDate = re.compile(r'"开业时间","attrValue":"(.*?)"')  # 输出 2018年
        find_DecDate = re.compile(r'"attrDesc":"装修时间","attrValue":"(.*?)"')  # 输出 2018年
        find_DescInfo = re.compile(r'"poiDesc":"(.*?)"')  # 酒店简介
        find_position = re.compile('"position":{(.*?)}')  # 经纬度

        # 解析查找
        res.encoding = 'uft-8'
        soup = BeautifulSoup(res.text, "html.parser")
        soup = str(soup)

        add_info['name'] = re.findall(find_name, soup)
        add_info['phone'] = re.findall(find_phone, soup)

        add_info['房间总量'] = re.findall(find_RoomsNum, soup)
        if len(re.findall(find_RoomsNum, soup)) <= 0:
            add_info['房间总量'] = " "
        else:
            add_info['房间总量'] = re.findall(find_RoomsNum, soup)[0]

        add_info['开业时间'] = re.findall(find_OpenDate, soup)
        if len(re.findall(find_OpenDate, soup)) == 0:
            add_info['开业时间'] = " "
        else:
            add_info['开业时间'] = re.findall(find_OpenDate, soup)[0]

        add_info['装修时间'] = re.findall(find_DecDate, soup)
        if len(re.findall(find_DecDate, soup)) == 0:
            add_info['装修时间'] = " "
        else:
            add_info['装修时间'] = re.findall(find_DecDate, soup)[0]

        add_info['酒店简介'] = re.findall(find_DescInfo, soup)
        add_info['经度'] = re.findall(find_position, soup)

        return add_info


if __name__ == '__main__':
    main()


