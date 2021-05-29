"""
-*- coding: utf-8 -*-
@Time :  2021-05-16 15:31
@Author : nanfang
"""
import os
import sys
from threading import Thread

import requests
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QPushButton
from guiqwt.tests.png_test import app
from lxml import etree
import re
import time as times
import csv
from components.dialog_exam_info import *
class Exam_Info_Dialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(Exam_Info_Dialog, self).__init__()
        self.setupUi(self)
        self.base_url = 'http://muchong.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.master_url = 'http://muchong.com/f-430-{}-threadtype-11-typeid-2304'
        self.heads = ["title", "url", "author", "time", "school", "major", "need_people"]
        self.save_path = r'E:/school_info.csv'
        self.page_list = []
        self.chapter_list = []
        self.model = ''
        self.Threads = []  # 线程队列
        self.btn_search.clicked.connect(self.download_exam_info)
        self.btn_download.clicked.connect(self.save_Excel)#保存为excel
        self.table.setColumnCount(8)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(['发布时间','学校', '专业', '年级','招生人数', '招生状态','具体内容', '原文地址'])
        self.info={}
        self.infos=[]
        self.heads =['发布时间', '学校', '专业', '年级', '招生人数', '招生状态', '具体内容', '原文地址']
        self.edit_log.append("请在上方输入爬取页数")
        self.edit_log.append("每页有100条调剂信息，最多爬取200页")


    def download_exam_info(self):
        page_num=int(self.box_page_num.text())
        try:
            thread_1 = Thread(target=self.get_urls, args=(self.master_url,page_num))
            thread_1.daemon = 1 ##将此线程设置为守护线程，控制线程结束
            thread_1.start()
            self.Threads.append(thread_1)
        except:
            self.edit_log.append("Error: 无法启动线程")
    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)
    def get_urls(self,url,page_num):
        _num=0#记录页数
        i=1
        while i<page_num+1:
            response = requests.get(url=url.format(i), headers=self.headers).text
            HTML = etree.HTML(response)
            try:
                urls = HTML.xpath('//table/tbody//a[@class="a_subject"]/@href')
            except:
                self.edit_log.append("获取失败，重新获取第"+str(i)+"页数据")
                continue
            # msgs = HTML.xpath('//div[@class="forum_body xmc_line_lr"]/table/tbody//a[@class="a_subject"]/text()')
            self.edit_log.append("爬取第"+str(i)+"页内容，共" + str(len(urls)) + "条调剂信息")
            i += 1
            j=0
            while j<len(urls):
                try:
                    self.get_pag_msg(self.base_url + urls[j])
                except:
                    self.edit_log.append("获取失败，重新获取第" + str(_num) + "条数据")
                    continue
                j += 1
                _num += 1
                self.edit_log.append("获取第" + str(_num) + "条")
                times.sleep(0.1)
    def save_Excel(self):
        save_path = QFileDialog.getExistingDirectory(self, "请选择存储路径", "C:")
        if save_path == '' or save_path == "C:/":
            return
        save_path = save_path + '/' + "调剂信息" + '.csv'
        if not os.path.exists(save_path):
            with open(save_path, "w", encoding='utf-8-sig') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(self.heads)
        with open(save_path, "a+", newline='', encoding='utf-8-sig') as f:
            f_csv = csv.writer(f)
            for info in self.infos:
                row = [info['发布时间'], info['学校'], info['专业'],
                       info['年级'], info['招生人数'], info['招生状态'], info['具体内容'], info['原文地址']]
                f_csv.writerow(row)
    def get_pag_msg(self,page_url):
        response = requests.get(url=page_url, headers=self.headers).text
        HTML = etree.HTML(response)
        title = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]/h1//text()')
        content = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]/div[@class="t_fsz"]//tr//text()')
        school = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[2]//text()')
        major = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[3]//text()')
        grade = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[4]//text()')
        recept_num = HTML.xpath(
            '//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[5]//text()')
        state = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[6]//text()')
        time = HTML.xpath(
            '//tbody[@id="pid1"]//td[@class="pls_foot"]/div[@class="pls_info"]/em[@class="xmc_c9"]/a/text()')
        # info=['标题', '发布时间', '学校', '专业', '年级', '招生人数', '招生状态', '具体内容', '原文地址']
        # self.info['标题'] = self.list_to_str(title[2]).strip()
        self.info['发布时间'] = self.list_to_str(time[0]).strip()
        self.info['学校'] = self.list_to_str(school[1:]).strip()
        m_s=""
        for s in major[1:]:
            m_s=m_s+s.strip()+"     "
        self.info['专业'] = m_s
        self.info['年级'] = self.list_to_str(grade[1:]).strip()
        self.info['招生人数'] = self.list_to_str(recept_num[1:]).strip()
        self.info['招生状态'] = self.list_to_str(state[1:]).strip()
        msg = ''
        for s in content:
            msg += s.replace('\n', '').replace('\t', '')
        self.info['具体内容'] = msg.strip()
        self.info['原文地址'] = page_url.strip()
        self.infos.append(self.info)
        row_cnt = self.table.rowCount()  # 返回当前行数（尾部）
        self.table.insertRow(row_cnt)  # 尾部插入一行新行表格
        _time = QTableWidgetItem(self.info['发布时间'])  # 发布时间
        self.table.setItem(row_cnt, 0, _time)
        _school = QTableWidgetItem(self.info['学校'])  # 学校
        self.table.setItem(row_cnt, 1, _school)
        _major = QTableWidgetItem(self.info['专业'])  # 专业
        self.table.setItem(row_cnt, 2, _major)
        _grade = QTableWidgetItem(self.info['年级'])  # 发布时间
        self.table.setItem(row_cnt, 3, _grade)
        _recept_num = QTableWidgetItem(self.info['招生人数'])  # 学校
        self.table.setItem(row_cnt, 4, _recept_num)
        _state = QTableWidgetItem(self.info['招生状态'])  # 专业
        self.table.setItem(row_cnt, 5, _state)
        _msg = QTableWidgetItem(self.info['具体内容'])  # 发布时间
        self.table.setItem(row_cnt, 6,_msg)
        _page_url = QTableWidgetItem(self.info['原文地址'])  # 学校
        self.table.setItem(row_cnt, 7, _page_url)
        self.info={}
    def list_to_str(self,my_list):
        s = ""
        for l in my_list:
            s += str(l)
        return s
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    response = requests.get('http://muchong.com/f-430-1-threadtype-11-typeid-2304', headers=headers).text
    print(response)
