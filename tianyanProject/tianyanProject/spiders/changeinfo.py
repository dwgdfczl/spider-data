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
    name = 'changeinfo'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['http://www.tianyancha.com/']

    page_url = 'https://www.tianyancha.com/pagination/{}.xhtml?ps=10&pn={}&id={}'
    page = 1
    page1 =1
    content = 'changeinfo'
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
        page_total = response.xpath('//div[@id="_container_changeinfo"]/div[@class="company_pager"]/ul/@page-total').extract_first()
        if page_total:
            global company_id
            company_id = response.url.split('/')[-1]
            global pt
            pt = math.ceil(int(page_total)/10)
            url = self.page_url.format(self.content,self.page,company_id)
            yield scrapy.Request(url,callback=self.parse_page)
        else:
            item = TianyanprojectItem()
            changeinfo = response.xpath('//div[@class="block-data"]/div[@id="_container_changeinfo"]/table/tbody/tr')
            if changeinfo:
            	item['变更记录'] = []
            	for cha in changeinfo:
            		item5 = {}
            		item5['序号'] = cha.xpath('.//td[1]/text()').extract_first()
            		item5['变更时间'] = cha.xpath('.//td[2]/text()').extract_first()
            		item5['变更项目'] = cha.xpath('.//td[3]/text()').extract_first()
            		# item5['变更前'] = cha.xpath('.//td[4]/div/text()').extract_first()
            		change_before = cha.xpath('.//td[4]/div')
            		item5['变更前'] = change_before.xpath('string(.)').extract_first()
            		# item5['变更后'] = cha.xpath('.//td[5]/div//text()').extract_first()
            		change_after = cha.xpath('.//td[5]/div')
            		item5['变更后'] = change_after.xpath('string(.)').extract_first()
            		item['变更记录'].append(item5)
            else:
            	item['变更记录'] = '暂无变更记录'
            yield item

    def parse_page(self, response):
        item = TianyanprojectItem()
        changeinfo = response.xpath('//tbody/tr')
        if changeinfo:
        	item['变更记录'] = []
        	for cha in changeinfo:
        		item5 = {}
        		item5['序号'] = cha.xpath('.//td[1]/text()').extract_first()
        		item5['变更时间'] = cha.xpath('.//td[2]/text()').extract_first()
        		item5['变更项目'] = cha.xpath('.//td[3]/text()').extract_first()
        		# item5['变更前'] = cha.xpath('.//td[4]/div/text()').extract_first()
        		change_before = cha.xpath('.//td[4]/div')
        		item5['变更前'] = change_before.xpath('string(.)').extract_first()
        		# item5['变更后'] = cha.xpath('.//td[5]/div//text()').extract_first()
        		change_after = cha.xpath('.//td[5]/div')
        		item5['变更后'] = change_after.xpath('string(.)').extract_first()
        		item['变更记录'].append(item5)
        else:
        	item['变更记录'] = '暂无变更记录'
        yield item

        if self.page < pt:
            self.page += 1
            url = self.page_url.format(self.content,self.page,company_id)
            yield scrapy.Request(url,callback=self.parse_page)
    