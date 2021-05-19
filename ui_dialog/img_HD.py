"""
-*- coding: utf-8 -*-
@Time :  2021-05-16 15:46
@Author : nanfang
"""

import os
import re
import time
import urllib
from threading import Thread
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QPushButton, QGraphicsPixmapItem, QGraphicsScene, QLabel, \
    QWidget
from lxml import etree

from components.dialog_img_HD import *
from PyQt5 import QtWidgets,QtGui
class Img_Dialog_HD(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(Img_Dialog_HD, self).__init__()
        self.setupUi(self)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.model = ''
        self.Threads = []  # 线程队列
        self.max_width=450
        self.max_high=300
        self.high=0
        self.list_img.currentItemChanged.connect(self.image)  # 这是点击item会返回item的名称:ps我使用qtDesigner绘制的TabWidget。
        self.list_img.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)# 这里以滚动窗口显示)
        self.btn_search.clicked.connect(self.select)  # 关联事件

        ## 图片数据
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
        self.imgName = ""
        self.imgNameUrlEncoding = ""  # 图片名的URL编码
        self.pageCount = 0  # 获取图片页数
        self.intervalTime = 0.2  # 获取图片间隔时间(s)
        self.netbianHostUrl = "http://www.netbian.com"  # 主机地址
        self.file_name=''
        self.keyword=''
        self.img_num=0
    def select(self):
        self.keyword=self.edit_search.text()
        self.imgNameUrlEncoding = urllib.parse.quote(self.keyword, "/", encoding="gbk")
        # 选择存储文件夹
        cwd = QFileDialog.getExistingDirectory(self, "请选择存储路径", "C:")
        if cwd == '' or cwd == "C:/":
            return
        self.file_name = cwd + "/" + self.keyword
        # 判断文件夹是否存在，不存在则创建一个新的
        if not os.path.exists(self.file_name):
            os.mkdir(self.file_name)
        # 开启新线程
        thread = Thread(target=self.start)
        # 将此线程设置为守护线程
        thread.daemon = 1
        thread.start()
    def image(self):
        imagefile = self.list_img.currentItem().text()
        png = QtGui.QPixmap(imagefile)
        self.label_img.setPixmap(png)
        self.label_img.setScaledContents(True)  # 让图片自适应label大小

    def getHtml(self, url):
        page = requests.get(url)
        page.encoding = page.apparent_encoding
        # if page.status_code==200:
        #     print("页面获取成功！")
        # else:
        #     print("页面获取失败！\r"+page.status_code)
        return page.text

    def getImageUrl(self, page):
        urlList = r"/desk/[0-9]*.htm"
        imgUrl = re.findall(urlList, page)
        return imgUrl

    def getImageUrl1(self, page1):
        urlList = r"/desk/[0-9]*-{1,}[0-9]*x[0-9]*.htm"
        imgUrl = re.findall(urlList, page1)
        return imgUrl[0]  # 返回第一张

    def getImageUrl2(self, page2):
        urlList = r"http://\w*.\w*.\w*./file/[0-9]*/[0-9]*\w*.\w*.jpg"
        imgUrl = re.findall(urlList, page2)
        return imgUrl

    def start(self):
        netbianUrl = "http://www.netbian.com/e/sch/index.php?page=" + str(0) + "&keyboard=" + self.imgNameUrlEncoding
        response = requests.get(netbianUrl).text
        HTML = etree.HTML(response)
        urls = HTML.xpath('//div[@class="page"]/a/@href')
        self.pageCount = len(urls)
        self.edit_log.append("一共有" + str(self.pageCount) + "页图片")
        self.edit_log.append("一共有" + str(urls[0].split("totalnum=")[1]) + "张图片")
        for cou in range(self.pageCount):
            netbianUrl = "http://www.netbian.com/e/sch/index.php?page=" + str(
                cou) + "&keyboard=" + self.imgNameUrlEncoding
            page = self.getHtml(netbianUrl)  # 获取第一个页面
            imgUrl = self.getImageUrl(page)  # 获取第一个页面的第cou个URL
            for url in imgUrl:
                self.img_num += 1
                response = requests.get(self.netbianHostUrl + url).text
                HTML = etree.HTML(response)
                img_url = HTML.xpath('//div[@class="endpage"]/div[@class="pic"]//img/@src')[0]
                _url=self.file_name + '/{}.jpg'.format(self.img_num)
                with open(_url, 'wb') as f:
                    self.list_img.addItem(_url)
                    f.write(requests.get(img_url).content)
                    self.edit_log.append("下载第" + str(self.img_num) + "张图片")
        self.edit_log.append("ヾﾉ≧∀≦)o 共保存了" + str(self.img_num) + "张图片！")
        self.img_num=0
        self.pageCount=0
