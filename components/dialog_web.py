# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_web.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Web(object):
    def setupUi(self, Dialog_Web):
        Dialog_Web.setObjectName("Dialog_Web")
        Dialog_Web.resize(769, 613)
        self.btn_select = QtWidgets.QPushButton(Dialog_Web)
        self.btn_select.setGeometry(QtCore.QRect(410, 200, 93, 51))
        self.btn_select.setObjectName("btn_select")
        self.comboBox = QtWidgets.QComboBox(Dialog_Web)
        self.comboBox.setGeometry(QtCore.QRect(130, 290, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Dialog_Web)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Web)

    def retranslateUi(self, Dialog_Web):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Web.setWindowTitle(_translate("Dialog_Web", "Dialog"))
        self.btn_select.setText(_translate("Dialog_Web", "select"))
        self.comboBox.setItemText(0, _translate("Dialog_Web", "1"))
        self.comboBox.setItemText(1, _translate("Dialog_Web", "2"))
        self.comboBox.setItemText(2, _translate("Dialog_Web", "3"))
        self.comboBox.setItemText(3, _translate("Dialog_Web", "4"))
        self.comboBox.setItemText(4, _translate("Dialog_Web", "5"))
        self.comboBox.setItemText(5, _translate("Dialog_Web", "6"))
        self.comboBox.setItemText(6, _translate("Dialog_Web", "7"))
