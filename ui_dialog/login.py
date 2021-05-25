"""
-*- coding: utf-8 -*-
@Time :  2021-05-19 17:15
@Author : nanfang
"""
import sys


from components.dialog_login import *
from ui_dialog.register import *
from main import MyWindow
from utils.DB.LoginDB import *

class Login_Dialog(QtWidgets.QDialog, Ui_login):
    def __init__(self):
        super(Login_Dialog, self).__init__()
        self.setupUi(self)
        self.btn_login.clicked.connect(self.login)
        self.btn_apply.clicked.connect(self.register)
        self.db= LoginDB()
    def login(self):
        account=self.line_account.text()
        password=self.line_password.text()
        if account=="" or password=="":
            QtWidgets.QMessageBox.information(self, "错误", "账号密码不能为空，请重新输入！")
            return
        if self.db.login(account,password):
            myWin.show() # 打开主窗口
            self.close() # 关闭登录窗口
            sender = self.sender()
            print(sender.text() + '被按下了')
        else:
            QtWidgets.QMessageBox.information(self, "错误", "账号或密码错误，请重新输入")
    def register(self):
        # 创建子窗口实例
        self.dialog = Register_Dialog()
        # 显示子窗口
        self.dialog.show()
        self.dialog.exec_()
        pass
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 创建子窗口实例
    dialog = Login_Dialog()
    myWin = MyWindow()
    # 显示子窗口
    dialog.show()
    sys.exit(app.exec_())
