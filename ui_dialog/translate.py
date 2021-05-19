"""
-*- coding: utf-8 -*-
@Time :  2021-05-16 15:47
@Author : nanfang
"""
from components.dialog_translate import *
from PyQt5 import  QtWidgets
import urllib.request
import urllib.parse
import json


class Translate_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Translate_Dialog, self).__init__()
        self.setupUi(self)
        self.btn_translate.clicked.connect(self.translate)
        self.url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        self.data = {
            'i': '',
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': '15837372097486',
            'sign': '8b1c0f6b6654975dcd9f89bb92d2b446',
            'ts': '1583737209748',
            'bv': 'ec579abcd509567b8d56407a80835950',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }

    def translate(self):
        self.edit_english.setText("")
        content = self.edit_chinese.toPlainText()
        print(content)
        if content == '':
            return
        self.data['i'] = content
        data = urllib.parse.urlencode(self.data).encode('utf-8')  # 编码
        req = urllib.request.Request(self.url, data)
        # 伪装
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400')
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')  # 解码
        # json.loads()将json字符串转发成为字典，提取数据，打印
        a = json.loads(html)
        for target in a['translateResult']:
            for s in target:
                self.edit_english.append(s['tgt'])