from components.dialog import *
from spider.bilibili import Bilibili_Spider
from utils.utils import dictList2List


class Video_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Video_Dialog, self).__init__()
        self.setupUi(self)

        self.spider = Bilibili_Spider()

        self.btn_search.clicked.connect(self.search)

    def search(self):
        key = self.edit_search.text()

        videos = self.spider.parse(key, './out')
        videos = dictList2List(videos, ['title', 'watch_num', 'link'])
        self.fill_table(videos, ['标题', '播放量 ', 'av号'])

        # self.spider.download_video(videos[0], './out')
