"""
-*- coding: utf-8 -*-
@Time :  2021-04-15 15:45
@Author : nanfang
"""
import requests
import os
import re
import time
from lxml import etree


##获取搜索的所有小说，做成列表
class TXT:
    url = 'https://m.rmxsba.com/search.html'
    main_url = "https://m.rmxsba.com"
    headers = {
        'Cookie': '__cfduid=dd50fb1ed80a7d95c26140bec3bf9b0d71620107395; Hm_lvt_ff5a36d21942c35af99271f0b1999352=1620107389; Hm_lpvt_ff5a36d21942c35af99271f0b1999352=1620110682',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
    }
    page_list=[]
    chapter_list = []
    def download_TXT(self, searchkey):
        data = {
            'searchkey': searchkey,
        }
        response = requests.post(self.url, data=data, headers=self.headers)
        # 使用正则表达式获取总页数
        pagePattern = r"value=\"(/search/\d+/\d+.html)\""
        pageStrs = re.findall(pagePattern, response.text)
        for i in range(len(pageStrs)):
            pageStrs[i] = self.main_url + pageStrs[i]  # 得到总的小说页数
        print("已爬取所有页数")

        novel_list = []  # 获取全部小说地址并存到这里面
        for i in range(len(pageStrs)):
            response = requests.post(pageStrs[i], data=data, headers=self.headers)
            # 使用xpath
            html = etree.HTML(response.text)
            book_urls = html.xpath('//p[@class="bookname"]/a/@href')
            book_names = html.xpath('//p[@class="bookname"]/a/text()')
            author_names = html.xpath('//p[@class="data"]//a[@class="layui-btn layui-btn-xs layui-bg-cyan"]/text()')
            contents = html.xpath('//p[@class="intro"]/text()')
            # 得到最小的长度，防止出错
            min_length = len(book_urls)
            if min_length > len(book_names):
                min_length = len(book_names)
            elif min_length > len(author_names):
                min_length = len(author_names)
            elif min_length > len(contents):
                min_length = len(contents)
            for j in range(min_length):
                l = []
                l.append(self.main_url + book_urls[j])
                l.append("小说名：" + book_names[j])
                l.append("作者：" + author_names[j])
                novel_list.append(l)
            time.sleep(0.3)  # 每秒爬一次
            print("已爬取第" + str(i + 1) + "页小说，" + "本页一共" + str(min_length) + "本小说")
        print("共爬取了" + str(len(novel_list)) + "本小说")
        for novel in novel_list:
            print(novel)
            # 使用正则表达式
            # novelPattern = r"\"(/\d+/)\">([\u4e00-\u9fa5]+)</a>"
            # pattern=r".*class=\"layui-btn layui-btn-xs layui-bg-cyan\">([\u4e00-\u9fa5]+)</a>"
            # strs = re.findall(pattern, response.text)
            # strs_ = re.findall(novelPattern, response.text)
            # print(strs)
            # print()
            # print()
            # print(strs_)
            # main_url="https://m.rmxsba.com"
            # length=len(strs)
            # for j in range(length):
            #     l=list()
            #     l.append(main_url+strs[j][0])
            #     l.append(strs[j][1])
            #     novel_list.append(l)
            # time.sleep(0.3) #每秒爬一次

            # # novel_list.append(lis)

    ## 获取一本小说所有页数
    def get_all_page(self, novelUrl):
        response = requests.get(novelUrl, headers=self.headers)
        html = etree.HTML(response.text)
        ## 获取所有的页数 及多少章节
        pages_url=html.xpath('//select/option/@value')
        page_chapter=html.xpath('//select/option/text()')
        page_min_len = min(len(pages_url), len(page_chapter))
        for i in range(page_min_len):
            l=[]
            l.append(self.main_url+pages_url[i])
            l.append(page_chapter[i])
            self.page_list.append(l)
        #爬取所有页的章节
        for page in self.page_list:
            print("获取到" + page[1] + "的地址")
            self.get_page_chapters(page[0])
            time.sleep(0.5)
    def get_page_chapters(self,page_url):
        ## 获取本页所有章节的地址
        response = requests.get(page_url, headers=self.headers)
        html = etree.HTML(response.text)
        chapter_url = html.xpath('//ul[@class="read"]/li/a/@href')
        chapter_name = html.xpath('//ul[@class="read"]/li/a/text()')
        min_len = min(len(chapter_name), len(chapter_url))
        chapter_list=[]
        for i in range(min_len):
            l = []
            l.append(self.main_url + chapter_url[i])
            l.append(chapter_name[i])
            chapter_list.append(l)
        for chapter in chapter_list:
            time.sleep(0.3)
            self.download_chapter_text(chapter[0])

    ## 获取本章节的小说内容，并下载
    def download_chapter_text(self,chapter_url):
        response=requests.get(chapter_url,headers=self.headers)
        html=etree.HTML(response.text)
        title=html.xpath('//h1[@class="headline"]/text()')[0]
        content=html.xpath('//div[@class="content"]/p/text()')
        with open("txt.txt",'a',encoding='utf-8')as f:
            f.write(title+'\n')
            for line in content:
                f.write(line+'\n')
            f.write('\n')
        print('已下载 '+title)




# searchkey=input("请输入想要下载的小说名：")
# searchkey = "修仙"
# txt = TXT()
# # 小说名字
# # txt.download_TXT(searchkey)
# # 把获取的地址放到这里
# txt.get_all_page("https://m.rmxsba.com/149287/")

# novelUrl=input("请输入想要下载的小说网址：")
# downloadNovel(novelUrl)

