"""
python爬虫，爬取小木虫调剂信息
"""
import os
import requests
from lxml import etree
import time as times
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
master_url = 'http://muchong.com/f-430-{}-threadtype-11-typeid-2304'#硕士招生,调剂信息库
doctor_url='http://muchong.com/f-430-1-typeid-2303'#博士招生
heads =['发布时间', '学校', '专业', '年级', '招生人数', '招生状态', '具体内容', '原文地址']
save_path = r'E:/school_info.csv'
if not os.path.exists(save_path):
    with open(save_path, "w",encoding='utf-8-sig') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(heads)
base_url = 'http://muchong.com'
infos=[]
info= {}
def get_urls(url):
    _num=0
    response=requests.get(url=url.format(1), headers=headers).text
    HTML = etree.HTML(response)
    urls=HTML.xpath('//div[@class="forum_body xmc_line_lr"]/table/tbody//a[@class="a_subject"]/@href')
    msgs = HTML.xpath('//div[@class="forum_body xmc_line_lr"]/table/tbody//a[@class="a_subject"]/text()')
    print("爬取第一页内容，共"+str(len(urls))+"条调剂信息")
    for url in urls:
        get_pag_msg(base_url+url)
        _num+=1
        print("下载第"+str(_num)+"条")
        times.sleep(0.1)
    with open(save_path, "a+", newline='', encoding='utf-8-sig') as f:
        f_csv = csv.writer(f)
        for info in infos:
            row = [info['发布时间'], info['学校'], info['专业'],
                   info['年级'], info['招生人数'], info['招生状态'], info['具体内容'], info['原文地址']]
            f_csv.writerow(row)
def get_pag_msg(page_url):
    response = requests.get(url=page_url, headers=headers).text
    HTML = etree.HTML(response)
    title = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]/h1//text()')
    content=HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]/div[@class="t_fsz"]//tr//text()')
    school = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[2]//text()')
    major=HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[3]//text()')
    grade = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[4]//text()')
    recept_num = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[5]//text()')
    state = HTML.xpath('//tbody[@id="pid1"]//div[@class="plc_Con"]//table[@class="adjust_table"]//tr[6]//text()')
    time=HTML.xpath('//tbody[@id="pid1"]//td[@class="pls_foot"]/div[@class="pls_info"]/em[@class="xmc_c9"]/a/text()')
    # info=['标题', '发布时间', '学校', '专业', '年级', '招生人数', '招生状态', '具体内容', '原文地址']
    info['标题']=list_to_str(title[2]).strip()
    info['发布时间']=list_to_str(time[0]).strip()
    info['学校']=list_to_str(school[1:]).strip()
    info['专业']=list_to_str(major[1:]).strip()
    info['年级']=list_to_str(grade[1:]).strip()
    info['招生人数']=list_to_str(recept_num[1:]).strip()
    info['招生状态']=list_to_str(state[1:]).strip()
    msg = ''
    for s in content:
        msg += s.replace('\n','').replace('\t','')
    info['具体内容']=msg.strip()
    info['原文地址']=page_url.strip()
    infos.append(info)

def list_to_str(my_list):
    s=""
    for l in my_list:
        s+=str(l)
    return s
get_urls(master_url)