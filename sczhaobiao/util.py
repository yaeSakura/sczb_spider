#!/usr/bin/env python
# -*- coding:utf-8 -*-
import xlwt
import datetime
import pymysql.cursors
# 发邮件库
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header

import os

def write_xls(results):
    if results:
        f = xlwt.Workbook()
        l = list(results)
        # print('l_list:', l)
        sh = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
        row0 = [u'招标种类', u'标题', u'地区', u'招标时间', u'详细信息连接']
        for i in range(0, len(row0)):
            sh.write(0, i, row0[i])
        for j in range(0, len(l)):
            sh.write(j + 1, 0, l[j][0])
            sh.write(j + 1, 1, l[j][1])
            sh.write(j + 1, 2, l[j][2])
            sh.write(j + 1, 3, l[j][3])
            sh.write(j + 1, 4, l[j][4])

        c = datetime.datetime.now().strftime('%Y-%m-%d')
        path = '四川招标-%s.xls' % c
        f.save(path)
        return path

# 测试用
def w_xls_test():
    conn = pymysql.connect(host='localhost', port=3306,
                           user='root',
                           password='',
                           db='toubiao',
                           charset='utf8')
    cursor = conn.cursor()
    brief_sql_search = ("SELECT now_type,title,area,start_time,detail_url FROM `sczhaobiao` WHERE id <= 200")
    cursor.execute(brief_sql_search)
    results = cursor.fetchall()
    conn.commit()
    # return write_xls(results)
    return send_msg_html(results)



def send_email_xls(path):
    print('path:', path)
    _port = 465
    _email_host = 'smtp.qq.com'
    _user = '1668488211@qq.com'
    _pwd = 'reveqrhbrisdbjjb'
    # _to = '18281606248@163.com'
    _to = 'zchengfile@163.com'
    subject = '四川招标网招投标信息'
    # 如名字所示Multipart就是分多个部分
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = _user
    msg['To'] = _to
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    # ---这是文字部分---
    part = MIMEText('我是何子奇，这是四川招标网招投标信息。')
    msg.attach(part)
    # ---这是附件部分---
    # xls类型附件
    part = MIMEApplication(open(path, 'rb').read())
    # print('part:', part)
    part.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(part)
    # 登录服务器发邮件
    s = smtplib.SMTP_SSL(_email_host, timeout=30, port=_port)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.close()
    # os.remove(path)

# path = u'四川招标-2017-09-29.xls'
# send_email_xls(path)

def send_msg_html(results):
    '''
    以HTML形式发送招标信息
    '''
    l = list(results)
    text_msg = ''
    # print('list l is', l)
    _port = 465
    _email_host = 'smtp.qq.com'
    _user = '1668488211@qq.com'
    _pwd = 'reveqrhbrisdbjjb'
    _to = '18281606248@163.com'
    # _to = 'zchengfile@163.com'
    subject = '四川招标网招投标信息'
    # 如名字所示Multipart就是分多个部分
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = _user
    msg['To'] = _to
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    # 遍历查询集
    for j in range(len(l)):
        text_msg += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="%s">Link</a></td>' % \
                    (l[j][0], l[j][1], l[j][2], l[j][3], l[j][4])
    # print('*' * 60)
    # print('text_msg:', text_msg)
    # ---这是文字部分---
    part = MIMEText('<html><body><table><tr><th>招标种类</th><th>标题</th><th>地区</th><th>招标时间</th><th>详细信息连接</th></tr>'
                    + text_msg + '</table></body></html>', 'html', 'utf-8')
    msg.attach(part)
    # 登录服务器发邮件
    s = smtplib.SMTP_SSL(_email_host, timeout=30, port=_port)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.close()


w_xls_test()