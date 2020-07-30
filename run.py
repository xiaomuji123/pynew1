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
    mail(file)

def mail(file):                   #发送邮件
    #163邮箱服务器地址
    mail_host = "mail.yy.com"
    mail_user = "yy-monkeytest@yy.com"
    mail_pass = "Yy1233211234567"
    #邮件发送方邮箱地址
    sender = 'yy-monkeytest@yy.com'
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receiver = ['chenhaihe@yy.com']

    #设置eamil信息
    #添加一个MIMEmultipart类，处理正文及附件
    message = MIMEMultipart()
    #邮件主题
    message['Subject'] = '每天爬虫日报'
    #发送方信息
    message['From'] = sender
    #接受方信息
    message['To'] = receiver[0]

    #推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
    # with open('abc.html','r') as f:
    #     content1 = f.read()
    #设置html格式参数（即正文内容）
    content1 = '您的宝贝已到达，请查看附件'
    part1 = MIMEText(content1,'html','utf-8')

    #添加一个txt文本附件
    with open(file,'r')as h:
        content2 = h.read()
    #设置txt参数
    part2 = MIMEText(content2,'plain','utf-8')
    #附件设置内容类型，方便起见，设置为二进制流
    part2['Content-Type'] = 'application/octet-stream'
    #设置附件头，添加文件名
    part2.add_header('Content-Disposition', 'attachment', filename=file)

    message.attach(part1)
    message.attach(part2)

    try:
        server = smtplib.SMTP()
        # 连接到服务器
        server.connect(mail_host)
        # 登录到服务器
        server.login(mail_user, mail_pass)
        # 发送
        server.sendmail(sender, receiver, message.as_string())
        # 退出
        server.close()
        print('邮件发送成功')
    except Exception as e:
        print('email exception', str(e))

# def main(h=14, m=23):         #定时爬取
#     while True:
#         now = datetime.datetime.now()
#         # print(now.hour, now.minute)
#         if now.hour == h and now.minute == m:
#             reptile()
#         # 每隔60秒检测一次
#         time.sleep(60)
#
# main()

reptile()