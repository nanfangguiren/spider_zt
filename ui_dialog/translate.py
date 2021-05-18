"""
-*- coding: utf-8 -*-
@Time :  2021-05-16 15:47
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


class Translate_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Translate_Dialog, self).__init__()
        self.setupUi(self)
        self.Request_URL = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.form_data = {}
        self.form_data['i'] = ''
        self.form_data['from'] = 'AUTO'
        self.form_data['to'] = 'AUTO'
        self.form_data['smartresult'] = 'dict'
        self.form_data['doctype'] = 'json'
        self.form_data['version'] = '2.1'
        self.form_data['keyfrom'] = 'fanyi.web'
        self.form_data['action'] = 'FY_BY_CLICKBUTTION'
        self.form_data['typoResult'] = 'false'





