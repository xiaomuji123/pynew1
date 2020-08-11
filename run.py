# coding:utf8
import datetime
import time
import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def reptile():         #爬取新闻头条
    print('.................开始爬虫...............')
    Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    headers = {'User-Agent': Agent}
    url = 'http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1'
    req = requests.get(url, headers=headers)
    # print(html.encoding)
    # req.encoding='GBK'
    # print(req.text)
    xml = etree.HTML(req.content)
    dict2 = {}
    for i in range(2, 52):
        title = '//*[@id="main"]/div[2]/div/table/tr[' + str(i) + ']/td[2]/a[1]/text()'  # 获取标题路径
        conut = '//*[@id="main"]/div[2]/div/table/tr[' + str(i) + ']/td[4]/span/text()'  # 获取热度路径
        # print(b)
        date1 = xml.xpath(title)  # 获取标题
        date2 = xml.xpath(conut)  # 获取热度
        dict1 = dict(zip(date1, date2))
        # print(date1)
        # print(date2)
        dict2.update(dict1)

    now = datetime.datetime.now().strftime('%Y%m%d %H%M')  #当前时间
    file = now+'.txt'
    with open(file, 'w') as f:
        for item in dict2.items():
            f.write(str(item))
            f.write('\n')
    print('.................爬虫结束...............')
    
if __name__ == '__main__':
    print("走你")
    reptile()
    print("搞完收工~")
