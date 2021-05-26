from utils.logger import Logger
import csv
import time
import urllib
from urllib.request import urlopen
import urllib.request
import requests
import numpy as np
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import json
import random
import gzip
from utils.video import merge_video_audio
from utils.utils import *
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)
sys.path.append(os.path.dirname(__file__))


# 防止因https证书问题报错
requests.packages.urllib3.disable_warnings()



class Bilibili_Spider():

    def __init__(self, logger=None):
        self.url = 'https://search.bilibili.com/all?keyword={0}&page={1}'
        self.header_list = [
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
            {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"},
            {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"},
            {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"},
            {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"},
            {'User-Agent': "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
            {'User-Agent': 'Opera/9.25 (Windows NT 5.1; U; en)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
            {'User-Agent': 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
            {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7"},
            {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "},
        ]
        self.proxy_list = [
            '45.119.208.134:80',
            '49.75.59.242:3128',
            '18.139.173.12:3128',
            '52.54.80.215:80',
            '3.225.148.200:80',
            '3.224.69.117:80',
            '116.117.134.135:8081',
        ]
        self.total_page_num = None
        self.save_header = ['link', 'title', 'watch_num',
                            'video_audio_split_flag', 'videoURL', 'audioURL']

        # 设置logger
        if logger is None:
            self.logger = Logger(show_mode='console_only')
        else:
            self.logger = logger

        self.random_proxy()

        
    def parse(self, keyword, outdir='./', useold=True, batch_fill_videos=None):
        # 可使用已保存的数据
        path = os.path.join(outdir, f'Bilibili_{keyword}.csv')
        if useold and os.path.exists(path):
            self.video_list = load_csv(path)
            self.logger.log(f'已加载旧数据 from {path}')
            return self.video_list

        # 搜索视频
        page_num = 1
        try_times = 0
        self.total_page_num = None
        video_list = []

        self.logger.log(f'开始搜索视频【{keyword}】...')
        while True:
            time.sleep(np.random.rand()/2 + 0.5)

            part_video_list = self._parse_one_page_(keyword, page_num)

            # 某一页错误最多重复执行 3 次
            if part_video_list is None and try_times < 5:
                try_times += 1
                self.logger.log(f'[再次尝试] page：{page_num} 重试')
                continue
            elif part_video_list is None:
                try_times = 0
                self.logger.log(f'[放弃] page：{page_num} 放弃重试')

            page_num += 1
            if part_video_list is not None:
                video_list.extend(part_video_list)
                self.logger.log(
                    f'[成功] page：{page_num-1} 成功加载，已有视频数：{len(video_list)}')

            # 总页数
            if self.total_page_num is not None and page_num > self.total_page_num:
                self.video_list = video_list
                break

        self.logger.log('视频av号已获取，进一步获取视频下载地址...')

        # 进一步获取视频 URL
        for index, video in enumerate(self.video_list):
            self.random_proxy()
            data = self._parse_video_url_(video['link'])
            video['videoURL'] = data['videoURL']
            video['audioURL'] = data['audioURL']
            video['video_audio_split_flag'] = data['video_audio_split_flag']
            self.logger.log(
                f'[成功] 已获取视频 {index+1} 下载地址 for 【{video["title"][:20]}...】')
            if batch_fill_videos is not None:
                batch_fill_videos([video])

        # 保存数据到 csv
        path = os.path.join(outdir, f'Bilibili_{keyword}.csv')
        save_csv(self.video_list, path)
        self.logger.log(f'[保存成功] 已保存数据到 {path}')

        return self.video_list

    def _parse_one_page_(self, keyword, page_num):
        header = self.header_list[page_num % len(self.header_list)]
        url = self.url.format(urllib.parse.quote(keyword), page_num)

        try:
            req = urllib.request.Request(url, headers=header)
            res = urllib.request.urlopen(req).read().decode('utf-8')
        except Exception as e:
            self.logger.log(
                f"[Error] 下载错误 page_num: {page_num}\t关键词：【{keyword}】")
            return None

        html = etree.HTML(res)

        video_list = []
        for video in html.xpath('//ul[contains(@class, "video-list")]/li'):
            data = {}

            data['title'] = video.xpath(
                './/a[contains(@class, "title")]/@title')[0]
            data['watch_num'] = video.xpath(
                './/span[contains(@class, "watch-num")]//text()')[0].strip()

            link = video.xpath('.//a[contains(@class, "title")]/@href')[0]
            link = re.findall('video/([\w]*)\?*', link)[0]
            data['link'] = link

            video_list.append(data)

        # 首次未初始化页面总数时，获取总页数
        if self.total_page_num == None:
            num = html.xpath(
                '//div[contains(@class, "pager")]//li[last()-1]//text()')
            num = int(num[0].strip()) if num != [] else 1
            self.total_page_num = num

        return video_list

    def _parse_video_url_(self, video_key):
        url = f'https://www.bilibili.com/video/{video_key}'
        header = self.header_list[random.randint(0, len(self.header_list)-1)]
        data = {}

        # session = requests.session()
        # res = session.get(url=url,headers=header,verify=False)

        req = urllib.request.Request(url, headers=header)
        res = urllib.request.urlopen(req).read()
        res = gzip.decompress(res).decode('utf-8')
        html = etree.HTML(res)

        # 获取window.__playinfo__的json对象,[20:]表示截取'window.__playinfo__='后面的json字符串
        videoPlayInfo = str(html.xpath(
            '//head/script[5]/text()')[0].encode('utf-8').decode('utf-8'))[20:]
        videoJson = json.loads(videoPlayInfo)

        # 获取视频链接和音频链接
        try:
            # 2018年以后的b站视频由.audio和.video组成 flag=0表示分为音频与视频
            data['videoURL'] = videoJson['data']['dash']['video'][0]['baseUrl']
            data['audioURL'] = videoJson['data']['dash']['audio'][0]['baseUrl']
            data['video_audio_split_flag'] = True
        except Exception:
            # 2018年以前的b站视频音频视频结合在一起,后缀为.flv flag=1表示只有视频
            data['videoURL'] = videoJson['data']['durl'][0]['url']
            data['video_audio_split_flag'] = False

        return data

    def download(self, video, outdir):
        # 没有 outdir 则创建
        if not os.path.exists(outdir):
            os.makedirs(outdir)
            self.logger.log(f'[info] 创建目录{outdir}')

        url = f'https://www.bilibili.com/video/{video["link"]}'
        header = self.header_list[random.randint(0, len(self.header_list)-1)]

        session = requests.session()
        res = session.get(url=url, headers=header, verify=False)

        v_path = os.path.join(outdir, f'video_{video["title"]}.mp4')
        a_path = os.path.join(outdir, f'audio_{video["title"]}.mp4')

        self.logger.log('[info] 正在下载视频')
        self._download_file_(
            video_key=video['link'], url=video['videoURL'], path=v_path, session=session)
        self.logger.log('【成功】 下载视频成功')

        if video['video_audio_split_flag']:
            self.logger.log('[info] 正在下载的音频')
            self._download_file_(
                video_key=video['link'], url=video['audioURL'], path=a_path, session=session)
            self.logger.log('【成功】 下载音频成功')

        self.logger.log('[info] 正在合并视频音频...')
        merge_video_audio(
            v_path.encode("utf-8").decode("utf-8"),
            a_path.encode("utf-8").decode("utf-8"),
            os.path.join(outdir, f'{video["title"]}.mp4')
        )
        self.logger.log('[成功] 合并视频音频成功！')

    def _download_file_(self, video_key, url, path, session):
        # 添加请求头键值对,写上 refered:请求来源
        header = self.header_list[random.randint(0, len(self.header_list)-1)]
        header.update(
            {'Referer': f'https://www.bilibili.com/video/{video_key}'}
        )

        # 发送option请求服务器分配资源
        session.options(url=url, headers=header, verify=False)

        # 指定每次下载1M的数据
        begin = 0
        end = 1024 * 512 - 1
        is_done = False

        while True:
            # 添加请求头键值对,写上 range:请求字节范围
            header.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})

            # 获取视频分片
            res = session.get(url=url, headers=header, verify=False)

            if res.status_code not in [416, 200]:
                begin = end + 1
                end = end + 1024*512
            else:
                header.update({'Range': str(begin) + '-'})
                res = session.get(url=url, headers=header, verify=False)
                is_done = True

            with open(path, 'ab') as fp:
                fp.write(res.content)
                fp.flush()
            # data=data+res.content

            if is_done:
                fp.close()
                break

    def random_proxy(self):
        proxy = random.choice(self.proxy_list)
        proxy = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)


if __name__ == '__main__':
    parser = Bilibili_Spider()

    videos = parser.parse("斤斤计较军军", './out/Video')

    parser.download(videos[0], './out/Video')
