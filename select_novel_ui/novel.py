"""
-*- coding: utf-8 -*-
@Time :  2021-05-08 15:31
@Author : nanfang
"""
from components.dialog import *

class Child_select_novel(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(Child_select_novel, self).__init__()
        self.setupUi(self)