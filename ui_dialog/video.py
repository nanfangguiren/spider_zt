from components.dialog import *
from spider.bilibili import Bilibili_Spider
from utils.utils import dictList2List
from threading import Thread
from PyQt5.QtWidgets import QAbstractItemView


class Video_Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Video_Dialog, self).__init__()
        self.setupUi(self)

        self.dict_header = ['title', 'watch_num', 'link']
        self.header = ['标题', '播放量 ', 'av号']
        
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.spider = Bilibili_Spider(self.logger)

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
        video = {}
        video['title'] = self.table.item(row, 0).text()
        video['link'] = self.table.item(row, 2).text()

        try:
            searching = Thread(target=self.download_thread, args=(video,))
            searching.start()
        except:
            self.logger.log("Error: 无法启动线程")
    
    def search_thread(self, key):
        videos = self.spider.parse(key, './out', batch_fill_videos=self.batch_fill_videos)
        # videos = dictList2List(videos, self.dict_header)
        # self.fill_table(videos, self.header)

    def download_thread(self, video):
        self.spider.download(video, './out/Video')

    # 借助batch_fill_table来批量加载表格
    def batch_fill_videos(self, videos):
        data_list = dictList2List(videos, self.dict_header)
        self.batch_fill_table(data_list)
