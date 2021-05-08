from components.dialog import *


class Music_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Music_Dialog, self).__init__()
        self.setupUi(self)
