# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http.request import Request
from sczhaobiao.items import CommitItem,SczhaobiaoItem

class ProjectRjSpider(scrapy.Spider):
    name = "project_rj"
    # allowed_domains = ["http://sichuan.bidchance.com/tsp_510000_0_02_0_1.html"]
    # start_urls = ['http://http://sichuan.bidchance.com/tsp_510000_0_02_0_1.html/']
    headers = {
        'User - Agent': 'Mozilla / 5.0(WindowsNT6.1;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 58.0.3029.110Safari / 537.36',
    }

    def start_requests(self):
        end_page = 30
        for i in range(1, end_page):
            print(u'正在爬取第%s页' % i)
            url = "http://sichuan.bidchance.com/tsp_510000_0_02_0_%s.html" % i
            yield Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        key_words = [u'软件', u'大学', u'系统', u'地图', u'地理信息', u'开发', u'学院', u'学校']
        print('-' * 50)
        # print(response.body)
        invite_bids_msgs = response.xpath('//table[@id="lie"]/*')
        # print(invite_bids_msgs)
        for ib_msg in invite_bids_msgs:
            sczb_item = SczhaobiaoItem()
            title = ib_msg.xpath('.//td[2]/a/text()').extract()[0]
            # print('title_type:', type(title))
            for key_word in key_words:
                if key_word in title:
                    area = ib_msg.xpath('.//td[3]/a/text()').extract()[0]
                    start_time = ib_msg.xpath('.//td[4]/text()').extract()[0]
                    detail_url = ib_msg.xpath('.//td[2]/a/@href').extract()[0]
                    sczb_item['title'] = title
                    sczb_item['area'] = area
                    sczb_item['start_time'] = start_time
                    sczb_item['detail_url'] = detail_url
                    print('=' * 50)
                    # print('title:', title)
                    yield sczb_item
        yield CommitItem()
        time.sleep(2)
