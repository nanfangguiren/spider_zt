"""
-*- coding: utf-8 -*-
@Time :  2021-05-16 15:46
@Author : nanfang
"""

import os
import time
import urllib
from threading import Thread
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QPushButton, QGraphicsPixmapItem, QGraphicsScene, QLabel, \
    QWidget
from components.dialog_img import *
from PyQt5 import QtWidgets,QtGui
class Img_Dialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(Img_Dialog, self).__init__()
        self.setupUi(self)
        self.base_url = 'http://muchong.com'
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
        self.url = 'http://image.baidu.com/search/acjson?'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
        self.keyword =""
        self.paginator=""
        self.img_nums=0
        self.cwd=''
        self.file_name=''

    def select(self):
        self.keyword=self.edit_search.text()
        self.paginator=int(self.box_page_num.text())
        params = self.get_param()
        urls = self.get_urls(params)
        # 选择存储文件夹
        self.cwd = QFileDialog.getExistingDirectory(self, "请选择存储路径", "C:")
        if self.cwd == '' or self.cwd == "C:/":
            return
        self.file_name = self.cwd + "/" + self.keyword
        # 判断文件夹是否存在，不存在则创建一个新的
        if not os.path.exists(self.file_name):
            os.mkdir(self.file_name)
        # 开启新线程
        thread = Thread(target=self.get_image_url, args=(urls,))
        # 将此线程设置为守护线程
        thread.daemon = 1
        thread.start()
    def image(self):
        imagefile = self.list_img.currentItem().text()
        png = QtGui.QPixmap(imagefile)
        self.label_img.setPixmap(png)
        self.label_img.setScaledContents(True)  # 让图片自适应label大小

    def get_param(self):
        """
        获取url请求的参数，存入列表并返回
        :return:
        """
        keyword = urllib.parse.quote(self.keyword)
        params = []
        for i in range(1, self.paginator + 1):
            params.append(
                'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=1&latest=0&copyright=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn={}&rn={}&gsm=78&1557125391211='.format(
                    keyword, keyword, 10 * i,10))
        return params
    def get_urls(self, params):
        """
        由url参数返回各个url拼接后的响应，存入列表并返回
        :return:
        """
        urls = []
        for i in params:
            urls.append(self.url + i)
        return urls

    def get_image_url(self, urls):
        for i in range(len(urls)):
            image_url = []
            json_data = requests.get(urls[i], headers=self.headers).json()
            json_data = json_data.get('data')
            for js in json_data:
                if js:
                    image_url.append(js.get('thumbURL'))
            time.sleep(0.5)
            self.edit_log.append("获取第"+str(i+1)+"页，十张图片的地址")
            self.get_image(image_url)

    def get_image(self, image_url):
        for index, url in enumerate(image_url, start=1):
            with open(self.file_name + '/{}.jpg'.format(self.img_nums+1), 'wb') as f:
                f.write(requests.get(url, headers=self.headers).content)
                self.list_img.addItem(self.file_name + '/{}.jpg'.format(self.img_nums+1))
                self.img_nums+=1
                self.edit_log.append("下载第"+str(self.img_nums)+"张图片")
