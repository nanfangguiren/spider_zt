"""
-*- coding: utf-8 -*-
@Time :  2021-05-25 11:25
@Author : nanfang
"""
import sys


from components.dialog_rigister import *
from utils.DB.LoginDB import *

class Register_Dialog(QtWidgets.QDialog, Ui_Apply_Account):
    def __init__(self):
        super(Register_Dialog, self).__init__()
        self.setupUi(self)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_ok.clicked.connect(self.register)
        self.db= LoginDB()
    def register(self):
        account=self.account.text()
        password=self.password.text()
        password_again=self.password_again.text()
        if account=="" or password=="":
            QtWidgets.QMessageBox.information(self, "错误", "账号密码不能为空，请重新输入!")
            return
        if password!=password_again:
            QtWidgets.QMessageBox.information(self, "错误", "两次密码不一致，请重新输入!")
            return
        if self.db.register(account,password):
            QtWidgets.QMessageBox.information(self, "正确", "账号申请成功")
            return
