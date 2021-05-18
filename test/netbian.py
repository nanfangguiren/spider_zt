import requests
import urllib
import urllib.parse
import re
import urllib.request
import time
import os.path
from lxml import etree

class netbian():
    imgName=""
    imgNameUrlEncoding=""#图片名的URL编码
    pageCount=3#获取图片页数
    intervalTime=0.2#获取图片间隔时间(s)
    netbianHostUrl="http://www.netbian.com"#主机地址
    def __init__(self,keyboard,pageCount):
        self.imgName=keyboard
        self.pageCount=pageCount
        self.imgNameUrlEncoding=urllib.parse.quote(keyboard,encoding="gbk")
    def getHtml(self,url):
        page=requests.get(url)
        page.encoding=page.apparent_encoding
        # if page.status_code==200:
        #     print("页面获取成功！")
        # else:
        #     print("页面获取失败！\r"+str(page.status_code))
        return page.text

    def getImageUrl(self,page):
        urlList=r"/desk/[0-9]*.htm"
        imgUrl = re.findall(urlList,page)
        return imgUrl

    def getImageUrl1(self,page1):
        urlList=r"/desk/[0-9]*-{1,}[0-9]*x[0-9]*.htm"
        imgUrl=re.findall(urlList,page1)
        return imgUrl[0]#返回第一张

    def start(self):
        netbianUrl = "http://www.netbian.com/e/sch/index.php?" + "page=1" + "&keyboard=" + self.imgNameUrlEncoding
        # 获取所有的页数
        search_page = self.getHtml(netbianUrl)  # 获取第一个页面
        html = etree.HTML(search_page)
        pages_list=html.xpath('//div[@class="page"]/a/@href')
        pageCount=len(pages_list)
        print(pages_list)
        print("一共"+str(pageCount)+"页图片-------开始下载---------")
        imageSaveCount=0#成功保存的图片数量
        for i in range(pageCount):
            netbianUrl = "http://www.netbian.com/e/sch/index.php?page="+str(i)+"&keyboard=" + self.imgNameUrlEncoding
            page = self.getHtml(netbianUrl)  # 获取第一个页面
            imgUrl = self.getImageUrl(page)  # 获取第一个页面所有的URL
            #获得所有图片的准确地址
            for j in range(len(imgUrl)):
                page1 = self.getHtml(self.netbianHostUrl + imgUrl[j])# 获取图片网页代码
                imgUrl1 = self.getImageUrl1(page1)# 获取第高清图片网页地址
                page2 = self.getHtml(self.netbianHostUrl + imgUrl1) # 获取高清图片的网页代码
                html=etree.HTML(page2)
                imgUrl2=html.xpath('//table[@id="endimg"]//img/@src')
                if len(imgUrl2)==0:
                    print("当前图片不存在,结束")
                    continue
                time.sleep(self.intervalTime)
                if not os.path.exists(os.getcwd()+"\\image"):#当前路径是否存在image文件夹
                    os.mkdir(os.getcwd()+"\\image")
        print("ヾﾉ≧∀≦)o 共保存了"+str(imageSaveCount)+"张图片！")

if __name__ == "__main__":
    keyword = "斗罗大陆"
    bian=netbian(keyword,0)#参数说明(要搜索的图片名，页数)
    bian.start()
