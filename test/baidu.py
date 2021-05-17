"""
-*- coding: utf-8 -*-
@Time :  2021-04-15 13:56
@Author : nanfang
"""

import requests
import os
import urllib

class Spider_baidu_image():
    def __init__(self):
        self.url = 'http://image.baidu.com/search/acjson?'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
        self.keyword = input("请输入搜索图片关键字:")
        self.paginator = int(input("请输入搜索页数，每页10张图片："))
    def get_param(self):
        """
        获取url请求的参数，存入列表并返回
        :return:
        """
        keyword = urllib.parse.quote(self.keyword)
        params = []
        for i in range(1, self.paginator + 1):
            params.append(
                'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=1&latest=0&copyright=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn={}&rn={}&gsm=78&1557125391211='.format(
                    keyword, keyword, 10 * i,10))
        return params
    def get_urls(self, params):
        """
        由url参数返回各个url拼接后的响应，存入列表并返回
        :return:
        """
        urls = []
        for i in params:
            urls.append(self.url + i)
        return urls

    def get_image_url(self, urls):
        image_url = []
        for url in urls:
            json_data = requests.get(url, headers=self.headers).json()
            json_data = json_data.get('data')
            for i in json_data:
                if i:
                    image_url.append(i.get('thumbURL'))
        # print(image_url)
        return image_url

    def get_image(self, image_url):
        """
        根据图片url，在本地目录下新建一个以搜索关键字命名的文件夹，然后将每一个图片存入。
        :param image_url:
        :return:
        """
        #  获得当前目录路径
        cwd = os.getcwd()
        # cwd=str(input('请输入存放路径:'))
        file_name = os.path.join(cwd, self.keyword)
        # 判断文件夹是否存在，不存在则创建一个新的
        if not os.path.exists(self.keyword):
            os.mkdir(file_name)
        for index, url in enumerate(image_url, start=1):
            with open(file_name + '\\{}.jpg'.format(index), 'wb') as f:
                f.write(requests.get(url, headers=self.headers).content)
            if index != 0 and index % 10 == 0:
                print('{}第{}页下载完成'.format(self.keyword, index / 10))

    def __call__(self, *args, **kwargs):
        params = self.get_param()
        urls = self.get_urls(params)
        image_url = self.get_image_url(urls)
        self.get_image(image_url)


if __name__ == '__main__':
    ## 根据地址读取网上图片，下载下来
    spider = Spider_baidu_image()
    spider()
