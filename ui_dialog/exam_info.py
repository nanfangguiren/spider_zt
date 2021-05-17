"""
-*- coding: utf-8 -*-
@Time :  2021-05-16 15:31
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
class Exam_Info_Dialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(Exam_Info_Dialog, self).__init__()
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
        self.Threads = []  # 线程队列
        # self.btn_search.clicked.connect(self.select)
        # self.table.doubleClicked.connect(self.download_novel)
        self.table.setHorizontalHeaderLabels(['书名', '作者', '地址'])
