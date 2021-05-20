"""
-*- coding: utf-8 -*-
@Time :  2021-05-20 16:38
@Author : nanfang
"""
import time
import requests
from lxml import etree
from pyecharts.charts import Pie
from pyecharts import options as opts
from PyQt5.QtCore import QUrl

import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from components.dialog_web import *
from PyQt5 import QtWidgets


class Web_Dialog(QtWidgets.QDialog, Ui_Dialog_Web):
    def __init__(self):
        super(Web_Dialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('百度')  # 窗口标题
        self.setGeometry(5, 30, 1355, 730)  # 窗口的大小和位置设置
        self.browser = QWebEngineView()
        # 加载外部的web界面
        self.browser.load(QUrl('F:/code/python/spider/view/test/饼状图_测试.html'))
        self.browser.show()

        # 小说数据分析部分
        self.ranking_url = "https://m.rmxsba.com/top.html"
        self.main_url = "https://m.rmxsba.com"
        self.headers = {
            'Cookie': '__cfduid=dd50fb1ed80a7d95c26140bec3bf9b0d71620107395; Hm_lvt_ff5a36d21942c35af99271f0b1999352=1620107389; Hm_lpvt_ff5a36d21942c35af99271f0b1999352=1620110682',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
        }
        self.web_title = "热门小说吧"
        self.btn_select.clicked.connect(self.HTML_select)
        self.comboBox.currentTextChanged.connect(self.show_data)
        # self.setCentralWidget(self.browser)
        # self.browser = QWebEngineView(Web_Dialog)


    def HTML_select(self):
        self.comboBox.addItem('k','v')
        self.browser.load(QUrl("E:/file/小说/推荐榜_总榜.html"))
        self.browser.show()
    def show_data(self):
        print(self.comboBox.currentData())
    # 得到所有的排行榜信息
    def get_dict_urls(self) -> dict:
        response = requests.get(self.ranking_url, headers=self.headers, timeout=2)
        html = etree.HTML(response.text)
        hrefs = html.xpath('//ul[@class="top"]/li/a/@href')
        hrefs_msg = html.xpath('//ul[@class="top"]/li/a/text()')
        rank_urls_dic = dict()
        for i in range(len(hrefs_msg)):
            if i < 4:
                rank_urls_dic["点击榜_" + hrefs_msg[i]] = self.main_url + hrefs[i]
            elif i == 4 or i == 5 or i == 6 or i == 11:
                continue
            elif i == 7:
                rank_urls_dic["推荐榜_" + hrefs_msg[i]] = self.main_url + hrefs[i]
            else:
                rank_urls_dic[hrefs_msg[i]] = self.main_url + hrefs[i]

        for k, url in rank_urls_dic.items():
            sort_list = self.get_url_data(url)
            dic = self.info_nums(sort_list)
            self.date_analyse_html(k, dic)
        return rank_urls_dic

    # 示例画图
    def date_analyse_html(self, html_title: str, dic: dict):
        key_list = []
        num_list = []
        for k, v in dic.items():
            key_list.append(k)
            num_list.append(v)
        pie = (Pie()
               .add('', [list(z) for z in zip(key_list, num_list)],
                    radius=["0%", "75%"],
                    )
               .set_global_opts(title_opts=opts.TitleOpts(title=self.web_title, subtitle=html_title),
                                legend_opts=opts.LegendOpts(
                                    orient="vertical",  # 竖向显示
                                    pos_left="85%",  # 距离左边85%
                                    type_="scroll"  # 滚动翻页图例
                                )
                                )
               .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
               )

        pie.render(html_title + ".html")
        self.browser = QWebEngineView()
        # 加载外部的web界面
        self.browser.load(QUrl('F:/code/python/spider/view/test/' + html_title + '.html'))
        self.browser.show()

    # 根据排行榜地址，得到确定排行榜前10页内容
    def get_url_data(self, url: str) -> list:
        sort_list = []
        for i in range(1, 11):
            print(url)
            response = requests.get(url, headers=self.headers, timeout=2)
            html = etree.HTML(response.text)
            sort_list.extend(html.xpath(
                '//ul[@class="list"]/li//p[@class="data"]/span[@class="layui-btn layui-btn-xs layui-btn-radius"]/text()'))
            url = url.replace("_" + str(i), "_" + str(i + 1))  # 修改地址
            time.sleep(0.1)
        return sort_list

    # 统计词频
    def info_nums(self, sort_list: list) -> dict:
        dic = dict()
        for msg in sort_list:
            dic[msg] = dic.get(msg, 0) + 1
        return dic


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 创建子窗口实例
    dialog = Web_Dialog()
    # 显示子窗口
    dialog.show()
    sys.exit(app.exec_())
