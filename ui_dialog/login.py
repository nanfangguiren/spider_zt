"""
-*- coding: utf-8 -*-
@Time :  2021-05-19 17:15
@Author : nanfang
"""
import sys

from PyQt5.QtWidgets import QApplication

from components.dialog_login import *
from PyQt5 import QtWidgets

from main import MyWindow


class Login_Dialog(QtWidgets.QDialog, Ui_login):
    def __init__(self):
        super(Login_Dialog, self).__init__()
        self.setupUi(self)
        self.btn_login.clicked.connect(self.login)
        # self.table.doubleClicked.connect(self.download_novel)
    def login(self):
        account=self.line_account.text()
        password=self.line_password.text()
        if account=="123456" and password=="123456":
            myWin.show() # 打开主窗口
            self.close() # 关闭登录窗口
            sender = self.sender()
            print(sender.text() + '被按下了')
        else:
            QtWidgets.QMessageBox.information(self, "错误", "账号或密码错误，请重新输入")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 创建子窗口实例
    dialog = Login_Dialog()
    myWin = MyWindow()
    # 显示子窗口
    dialog.show()
    sys.exit(app.exec_())
