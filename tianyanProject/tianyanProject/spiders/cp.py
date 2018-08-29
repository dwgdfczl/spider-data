# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import requests
import time
import math
import re
from ..settings import COOKIES,DEFAULT_REQUEST_HEADERS,headers2
from ..items import TianyanprojectItem

class CpSpider(scrapy.Spider):
    name = 'cp'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['http://www.tianyancha.com/']

    page_url = 'https://www.tianyancha.com/pagination/{}.xhtml?ps=20&pn={}&id={}'
    page = 1
    content = 'copyright'
    # id = 22822
    company_name = ''

    def start_requests(self):
        f = open('companylist', 'r')
        for obj in f:
            DEFAULT_REQUEST_HEADERS["Referer"] = "https://www.tianyancha.com/"
            global company_name
            self.company_name = obj
            # global company_id
            # company_id = ''
            self.url1 = "https://www.tianyancha.com/search?key=%s" % (urllib.parse.quote(self.company_name))
            yield scrapy.Request(self.url1, cookies=COOKIES,callback=self.parse)

    def parse(self, response):
        headers2["Referer"] = self.url1
        infos = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/a/@href').extract_first()
        yield scrapy.Request(url=infos, callback=self.parse_info)

    def parse_info(self, response):
        page_total = response.xpath('//div[@id="_container_copyright"]/div[@class="company_pager"]/ul/@page-total').extract_first()
        if page_total:
            global company_id
            company_id = response.url.split('/')[-1]
            global pt
            pt = math.ceil(int(page_total)/20)
            url = self.page_url.format(self.content,self.page,company_id)
            yield scrapy.Request(url,callback=self.parse_page)
        else:
            item = TianyanprojectItem()
            copyright = response.xpath('//div[@class="block-data"]/div[@id="_container_copyright"]/table/tbody/tr')
            if copyright:
                item['软件著作权'] = []
                for cr in copyright:
                    item29 = {}
                    item29['序号'] = cr.xpath('.//td[1]/text()').extract_first()
                    item29['批准日期'] = cr.xpath('.//td[2]/span/text()').extract_first()
                    item29['软件全称'] = cr.xpath('.//td[3]/span/text()').extract_first()
                    item29['软件简称'] = cr.xpath('.//td[4]/span/text()').extract_first()
                    item29['登记号'] = cr.xpath('.//td[5]/span/text()').extract_first()
                    item29['分类号'] = cr.xpath('.//td[6]/span/text()').extract_first()
                    item29['版本号'] = cr.xpath('.//td[7]/span/text()').extract_first()
                    item['软件著作权'].append(item29)
            else:
                item['软件著作权'] = '暂无软件著作权信息'
            yield item

    def parse_page(self, response):
        item = TianyanprojectItem()
        copyright = response.xpath('//tbody/tr')
        if copyright:
            item['软件著作权'] = []
            for cr in copyright:
                item4 = {}
                item4['序号'] = cr.xpath('.//td[1]/text()').extract_first()
                item4['批准日期'] = cr.xpath('.//td[2]/span/text()').extract_first()
                item4['软件全称'] = cr.xpath('.//td[3]/span/text()').extract_first()
                item4['软件简称'] = cr.xpath('.//td[4]/span/text()').extract_first()
                item4['登记号'] = cr.xpath('.//td[5]/span/text()').extract_first()
                item4['分类号'] = cr.xpath('.//td[6]/span/text()').extract_first()
                item4['版本号'] = cr.xpath('.//td[7]/span/text()').extract_first()
                item['软件著作权'].append(item4)
        else:
            item['软件著作权'] = '暂无软件著作权信息'

        yield item

        if self.page < pt:
            self.page += 1
            url = self.page_url.format(self.content,self.page,company_id)
            yield scrapy.Request(url,callback=self.parse_page)
    