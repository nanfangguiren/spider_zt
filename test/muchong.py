"""
python爬虫，爬取小木虫调剂信息
"""

import requests
from lxml import etree
import time as times
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
mu_url = 'http://muchong.com/f-430-{}'

heads = ["title", "url", "author", "time", "school", "major", "need_people"]
save_path = r'E:/school_info.csv'
with open(save_path, "w") as f:
    f_csv = csv.writer(f)
    f_csv.writerow(heads)
base_url = 'http://muchong.com'

for i in range(1, 5000):
    try:
        response = requests.get(url=mu_url.format(i), headers=headers).text
        HTML = etree.HTML(response)
        tbodys = HTML.xpath("//div[@class='forum_body xmc_line_lr']/table/tbody[position()>1]")
        infos = []
        for tbody in tbodys:
            try:
                title = tbody.xpath('.//a[@class="a_subject"]//text()')
                url = tbody.xpath('.//a[@class="a_subject"]/@href')
                author = tbody.xpath('.//th[@class="by"]/cite/a//text()')
                time = tbody.xpath('.//th[@class="by"]//nobr//text()')
                #     print(title[0] + " "+ base_url+ url[0]  + " " + author[0]+ " " + time[0])
                info = {}
                info['title'] = title[0]
                info['url'] = base_url + url[0]
                info['author'] = author[0]
                info['time'] = time[0]
                info_response = requests.get(info['url'], headers=headers).text
                info_HTML = etree.HTML(info_response)
                school = info_HTML.xpath("//table[@class='adjust_table']//tr[position()=2]/td[position()=2]//text()")[0]
                major = info_HTML.xpath("//table[@class='adjust_table']//tr[position()=3]/td[position()=2]//text()")[0]
                need_people = info_HTML.xpath("//table[@class='adjust_table']//tr[position()=5]/td[position()=2]//text()")[
                    0]
                info['school'] = school
                info['major'] = major
                info['need_people'] = need_people
                print(info)
                infos.append(info)
                times.sleep(0.001)
            except:
                print('路径错误')
    except:
        print("错误")

    with open(save_path, "a+", newline='') as f:
        f_csv = csv.writer(f)
        for info in infos:
            row = [info['title'].strip(), info['url'].strip(), info['author'].strip(), info['time'].strip(),
                   info['school'].strip(), info['major'].strip(), info['need_people'].strip()]
            try:
                f_csv.writerow(row)
            except:
                print("编码错误")
    times.sleep(0.1)
