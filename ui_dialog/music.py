from components.dialog import *
from spider.netease import Netease
from utils.utils import dictList2List
from threading import Thread
from PyQt5.QtWidgets import QAbstractItemView


class Music_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Music_Dialog, self).__init__()
        self.setupUi(self)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['标题', '作者 ', '下载地址'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.spider = Netease(logger=self.logger)

        self.btn_search.clicked.connect(self.search)
        self.table.doubleClicked.connect(self.download)

    def search(self):
        key = self.edit_search.text()

        try:
            searching = Thread(target=self.search_thread, args=(key,))
            searching.start()
        except:
            self.logger.log("Error: 无法启动线程")

    def download(self, line):
        row = line.row()
        song = {}
        song['name'] = self.table.item(row, 0).text()
        song['author'] = self.table.item(row, 1).text()
        song['url'] = self.table.item(row, 2).text()

        try:
            searching = Thread(target=self.download_thread, args=(song,))
            searching.start()
        except:
            self.logger.log("Error: 无法启动线程")

    def search_thread(self, key):
        self.logger.log(f'正在搜索音乐：{self.edit_search.text()}...')
        # 搜索 Key 的歌曲
        songs = self.spider.search(key, 20)
        songs = dictList2List(songs, ['name', 'author', 'url'])

        # 填充 songs 到表格
        self.fill_table(songs, ['标题', '作者 ', '下载地址'])

    def download_thread(self, song):
        self.spider.download(song, './out/Music')
    

