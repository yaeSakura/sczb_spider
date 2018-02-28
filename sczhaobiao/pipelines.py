#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
from sczhaobiao.items import CommitItem, SczhaobiaoItem
# 导入写成文档，发邮件方法
from sczhaobiao.util import write_xls, send_email_xls
# 导入异常类
from scrapy.exceptions import DropItem


class SczhaobiaoPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='root',
                                    password='',
                                    db='toubiao',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.brief_sql = ("INSERT IGNORE INTO `sczhaobiao`(title,area,start_time,detail_url)"
                          "VALUES(%s,%s,%s,%s)")

        self.need_drop_keywords = {'空调', '竞价', '乐器', '家具', '修缮工程', '农业', '打印',
                                   '投影', '供水系统', '电视设备', '床', '文件夹', '耗材', '校庆',
                                   '改造工程', '工程施工', '建设工程', '搬迁', '一批', '工作服',
                                   '调研', '农田', '餐具', '燃煤', '无轨', '洗衣机', '办公椅', '医学',
                                   '注射器', '培养皿', '广口瓶', '滴定管', '试剂瓶', '整治工程'}

    def process_item(self, item, spider):
        try:
            if isinstance(item, CommitItem):
                self.conn.commit()
            elif isinstance(item, SczhaobiaoItem):
                self.cursor.execute(self.brief_sql, (item['title'], item['area'],
                                                     item['start_time'], item['detail_url']))
            else:
                pass
        except Exception as e:
            spider.logger.warning("excute sql fail.")
            spider.logger.warning(str(e))
        return item

    def close_spider(self, spider):
        # 过滤数据库中的数据
        brief_sql_find = ("SELECT id,title FROM `sczhaobiao`")
        self.cursor.execute(brief_sql_find)
        find_results = self.cursor.fetchall()
        self.conn.commit()
        frls = list(find_results)
        print('frls:', frls)
        for need_drop_ketword in self.need_drop_keywords:
            for frl in frls:
                if need_drop_ketword in frl[1]:
                    print('frl[1]:', frl[1])
                    brief_sql_drop = ("DELETE FROM `sczhaobiao` WHERE id = %d" % frl[0])
                    self.cursor.execute(brief_sql_drop)

        self.brief_sql_search = ("SELECT now_type,title,area,start_time,detail_url FROM `sczhaobiao`")
        self.brief_sql_reset_table = ("TRUNCATE `sczhaobiao`")
        self.cursor.execute(self.brief_sql_search)
        results = self.cursor.fetchall()
        self.conn.commit()
        path = write_xls(results)
        # send_email_xls(path)
        # self.cursor.execute(self.brief_sql_reset_table)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print(u'这个爬虫关闭了')


# class FilterItemPipeline(object):
#     def __init__(self):
#         self.need_drop_keywords = {'空调', '竞价', '乐器', '家具', '修缮工程', '农业', '打印',
#                                    '投影', '供水系统', '电视设备', '床', '文件夹', '耗材', '校庆',
#                                    '改造工程', '工程施工', '建设工程', '搬迁', '一批', '工作服',
#                                    '调研', '农田', '餐具', '燃煤', '无轨', '洗衣机', '办公椅', '医学',
#                                    '注射器', '培养皿', '广口瓶', '滴定管', '试剂瓶', '整治工程'}
#
#     def process_item(self, item, spider):
#         for need_drop_keyword in self.need_drop_keywords:
#             # print('process_item_title:', item['title'])
#             if str(item['title']).count(need_drop_keyword) > 0:
#                 print('in if !!!!!!')
#                 raise DropItem('Need drop keywords in %s' % item)
#             else:
#                 print('this item is pass!!')
#         return item

