from components.dialog import *
# from spider.netease import Netease
from utils.utils import dictList2List


class Music_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Music_Dialog, self).__init__()
        self.setupUi(self)
        pass
        self.spider = Netease()

        self.btn_search.clicked.connect(self.search)

    
    def search(self):
        pass
        # key = self.edit_search.text()
        #
        # # 搜索 Key 的歌曲
        # songs = self.spider.search(key, 20)
        # songs = dictList2List(songs, ['name', 'author', 'url'])
        #
        # # 填充 songs 到表格
        # self.fill_table(songs, ['标题', '作者 ', '下载地址'])
