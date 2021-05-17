"""
-*- coding: utf-8 -*-
@Time :  2021-05-08 15:31
@Author : nanfang
"""
import time
from components.dialog import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from lxml import etree
import re


class Novel_Dialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(Novel_Dialog, self).__init__()
        self.setupUi(self)
        self.url = 'https://m.rmxsba.com/search.html'
        self.main_url = "https://m.rmxsba.com"
        self.headers = {
            'Cookie': '__cfduid=dd50fb1ed80a7d95c26140bec3bf9b0d71620107395; Hm_lvt_ff5a36d21942c35af99271f0b1999352=1620107389; Hm_lpvt_ff5a36d21942c35af99271f0b1999352=1620110682',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
        }
        self.page_list = []
        self.chapter_list = []
        self.model = ''
        self.Threads=[]  # 线程队列
        self.btn_search.clicked.connect(self.select)
        self.table.doubleClicked.connect(self.download_novel)
        self.table.setHorizontalHeaderLabels(['书名', '作者', '地址'])
      


    # 获取所有的小说名
    def download_TXT(self, searchkey):
        data = {
            'searchkey': searchkey,
        }

        response = requests.post(self.url, data=data, headers=self.headers)
        # 使用正则表达式获取总页数
        pagePattern = r"value=\"(/search/\d+/\d+.html)\""

        pageStrs = re.findall(pagePattern, response.text)
        for i in range(len(pageStrs)):
            pageStrs[i] = self.main_url + pageStrs[i]  # 得到总的小说页数
        self.edit_log.append("已爬取所有页数")

        novel_list = []  # 获取全部小说地址并存到这里面
        for i in range(len(pageStrs)):
            response = requests.post(pageStrs[i], data=data, headers=self.headers, timeout=5)
            # 使用xpath
            html = etree.HTML(response.text)
            book_urls = html.xpath('//p[@class="bookname"]/a/@href')
            book_names = html.xpath('//p[@class="bookname"]/a/text()')
            author_names = html.xpath('//p[@class="data"]//a[@class="layui-btn layui-btn-xs layui-bg-cyan"]/text()')
            contents = html.xpath('//p[@class="intro"]/text()')
            # 得到最小的长度，防止出错
            min_length = len(book_urls)
            if min_length > len(book_names):
                min_length = len(book_names)
            elif min_length > len(author_names):
                min_length = len(author_names)
            elif min_length > len(contents):
                min_length = len(contents)
            for j in range(min_length):
                l = []
                ##### tableweight 循环添加数据
                row_cnt = self.table.rowCount()  # 返回当前行数（尾部）
                self.table.insertRow(row_cnt)  # 尾部插入一行新行表格
                novel_item = QTableWidgetItem(book_names[j])  # 书名
                self.table.setItem(row_cnt, 0, novel_item)
                author_item = QTableWidgetItem(author_names[j])  # 作者名
                self.table.setItem(row_cnt, 1, author_item)
                address_item = QTableWidgetItem(self.main_url + book_urls[j])  # 地址
                self.table.setItem(row_cnt, 2, address_item)
                ######
                l.append(self.main_url + book_urls[j])
                l.append("小说名：" + book_names[j])
                l.append("作者：" + author_names[j])
                novel_list.append(l)
            time.sleep(0.3)  # 每0.3秒爬一次
            # 输出日志到界面中
            self.edit_log.append("已爬取第" + str(i + 1) + "页小说，" + "本页一共" + str(min_length) + "本小说")
        self.edit_log.append("共爬取了" + str(len(novel_list)) + "本小说")

    def select(self):
        # # 获取输入行中的信息
        try:
            self.edit_log.append(self.edit_search.text())
            thread_1 = Thread(target=self.download_TXT, args=(self.edit_search.text(),))
            thread_1.start()
        except:
            self.edit_log.append("Error: 无法启动线程")

    ## 获取一本小说所有页数
    def get_all_page(self, novelUrl, save_path):
        response = requests.get(novelUrl, headers=self.headers, timeout=2)
        html = etree.HTML(response.text)
        ## 获取所有的页数 及多少章节
        pages_url = html.xpath('//select/option/@value')
        page_chapter = html.xpath('//select/option/text()')
        page_min_len = min(len(pages_url), len(page_chapter))
        for i in range(page_min_len):
            l = []
            l.append(self.main_url + pages_url[i])
            l.append(page_chapter[i])
            self.page_list.append(l)

        # 爬取所有页的章节
        for page in self.page_list:
            self.edit_log.append("获取到" + page[1] + "的地址")
            self.get_page_chapters(page[0], save_path)

            time.sleep(0.5)

    def get_page_chapters(self, page_url, save_path):
        ## 获取本页所有章节的地址
        response = requests.get(page_url, headers=self.headers, timeout=2)
        html = etree.HTML(response.text)
        chapter_url = html.xpath('//ul[@class="read"]/li/a/@href')
        chapter_name = html.xpath('//ul[@class="read"]/li/a/text()')
        min_len = min(len(chapter_name), len(chapter_url))
        chapter_list = []
        for i in range(min_len):
            l = []
            l.append(self.main_url + chapter_url[i])
            l.append(chapter_name[i])
            chapter_list.append(l)
        for chapter in chapter_list:
            time.sleep(0.3)
            self.download_chapter_text(chapter[0], save_path)

    ## 获取本章节的小说内容，并下载
    def download_chapter_text(self, chapter_url, save_path):
        response = requests.get(chapter_url, headers=self.headers, timeout=2)
        html = etree.HTML(response.text)
        title = html.xpath('//h1[@class="headline"]/text()')[0]
        content = html.xpath('//div[@class="content"]/p/text()')
        with open(save_path, 'a', encoding='utf-8')as f:
            f.write(title + '\n')
            for line in content:
                f.write(line + '\n')
            f.write('\n')
        self.edit_log.append('已下载 ' + title)

    def download_novel(self, index):
        row = index.row()
        ##双击获取地址
        novel_name = self.table.item(row, 0).text()
        novel_author = self.table.item(row, 1).text()
        novel_url = self.table.item(row, 2).text()
        ## 选择存储文件夹
        save_path = QFileDialog.getExistingDirectory(self, "请选择存储路径", "C:")
        if save_path == '' or save_path == "C:/":
            return
        save_path = save_path + '/' + novel_name + '.txt'
        self.edit_log.append("下载地址为：" + save_path)
        self.edit_log.append("开始下载：" + novel_name)
        self.edit_log.append("作者：" + novel_author)
        # 开启新线程
        thread = Thread(target=self.get_all_page, args=(novel_url, save_path))
        # 将此线程设置为守护线程
        thread.daemon = 1
        thread.start()
        # 将线程加入线程队列
        self.Threads.append(thread)

