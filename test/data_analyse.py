"""
-*- coding: utf-8 -*-
@Time :  2021-05-20 14:21
@Author : nanfang
"""
import sys
import time
import requests
from lxml import etree
from pyecharts.charts import Pie
from pyecharts import options as opts

class novel_analyse():
    def __init__(self):
        # 小说数据分析部分
        self.ranking_url = "https://m.rmxsba.com/top.html"
        self.main_url="https://m.rmxsba.com"
        self.headers = {
            'Cookie': '__cfduid=dd50fb1ed80a7d95c26140bec3bf9b0d71620107395; Hm_lvt_ff5a36d21942c35af99271f0b1999352=1620107389; Hm_lpvt_ff5a36d21942c35af99271f0b1999352=1620110682',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
        }
        self.web_title="热门小说吧"
        self.html_title="饼状图_测试"

    #得到所有的排行榜信息
    def get_dict_urls(self)->dict:
        response = requests.get(self.ranking_url, headers=self.headers, timeout=2)
        html = etree.HTML(response.text)
        hrefs = html.xpath('//ul[@class="top"]/li/a/@href')
        hrefs_msg = html.xpath('//ul[@class="top"]/li/a/text()')
        rank_urls_dic=dict()
        for i in range(len(hrefs_msg)):
            if i<4:
                rank_urls_dic["点击榜_" + hrefs_msg[i]] = self.main_url + hrefs[i]
            elif i==4 or i==5 or i==6 or i==11:
                continue
            elif i==7:
                rank_urls_dic["推荐榜_"+hrefs_msg[i]] = self.main_url + hrefs[i]
            else:
                rank_urls_dic[hrefs_msg[i]]=self.main_url+hrefs[i]
        return rank_urls_dic

    # 示例画图
    def date_analyse_html(self,dic:dict):
        key_list = []
        num_list = []
        for k, v in dic.items():
            key_list.append(k)
            num_list.append(v)
        pie = (Pie()
               .add('', [list(z) for z in zip(key_list, num_list)],
                    radius=["0%", "75%"],
                    )
               .set_global_opts(title_opts=opts.TitleOpts(title=self.web_title, subtitle=self.html_title),
                                legend_opts=opts.LegendOpts(
                                    orient="vertical",  # 竖向显示
                                    pos_left="85%",  # 距离左边85%
                                    type_="scroll"  # 滚动翻页图例
                                )
        )
               .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
               )
        pie.render(self.html_title+".html")

    #根据排行榜地址，得到确定排行榜前10页内容
    def get_url_data(self,url:str)->list:
        sort_list=[]
        for i in range(1,11):
            print(url)
            response = requests.get(url, headers=self.headers, timeout=2)
            html = etree.HTML(response.text)
            sort_list.extend(html.xpath('//ul[@class="list"]/li//p[@class="data"]/span[@class="layui-btn layui-btn-xs layui-btn-radius"]/text()'))
            url = url.replace("_" + str(i), "_" + str(i + 1)) #修改地址
            time.sleep(0.2)
        return sort_list

    # 统计词频
    def info_nums(self,sort_list:list)->dict:
        dic=dict()
        for msg in sort_list:
            dic[msg]=dic.get(msg,0)+1
        return dic

# data = novel_analyse()
# sort_list=data.get_url_data("https://m.rmxsba.com/monthvisit_1/")
# dic=data.info_nums(sort_list)
# data.date_analyse_html(dic)
