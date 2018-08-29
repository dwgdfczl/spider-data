# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import requests
import time
import math
import re
from ..settings import COOKIES,DEFAULT_REQUEST_HEADERS,headers2
from ..items import TianyanprojectItem

class TycSpider(scrapy.Spider):
    name = 'tyc'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['https://www.tianyancha.com/']
    company_name = ''
    url = ''
    # page_url = 'https://www.tianyancha.com/pagination/icp.xhtml?ps=5&pn=2&id=22822'
    page_url = 'https://www.tianyancha.com/pagination/{}.xhtml?ps=5&pn={}&id={}'
    page_url1 = 'https://www.tianyancha.com/pagination/{}.xhtml?ps=5&pn={}&name={}'
    page = 1

    def start_requests(self):
        f = open('companylist', 'r')
        for obj in f:
            DEFAULT_REQUEST_HEADERS["Referer"] = "https://www.tianyancha.com/"
            global company_name
            self.company_name = obj
            self.url = "https://www.tianyancha.com/search?key=%s" % (urllib.parse.quote(self.company_name))
            yield scrapy.Request(self.url, cookies=COOKIES,callback=self.parse_page)

    def parse_page(self, response):
        headers2["Referer"] = self.url
        item = TianyanprojectItem()
        item['公司名'] = self.company_name

        reg_time = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[3]/span/@title').extract()
        item["注册时间"] = reg_time[0] if reg_time else '暂无注册时间信息'

        # tel = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[1]/span[2]/text()').extract()
        # item["电话"] = tel[0] if tel else '暂无电话信息'

        company_status = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/text()').extract()
        item["经营状态"] = company_status[0] if company_status else '暂无经营状态信息'

        reg_capital = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/span/text()').extract()
        item["注册资本"] = reg_capital[0] if reg_capital else '暂无注册资本信息'
        # 获取公司详情页链接
        infos = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/a/@href').extract_first()      
        if infos:
            DEFAULT_REQUEST_HEADERS["Referer"] = infos
            item["公司在天眼查的url"] = infos
            #获取商品id
            global company_id
            company_id = infos.split('/')[-1]
            yield scrapy.Request(url=infos, cookies=COOKIES, meta={'item': item}, callback=self.parse_info)
        else:
            item["公司在天眼查的url"] = '暂无该公司信息'
            yield item

    def parse_info(self, response):
        item = response.meta['item']

        tel = response.xpath(
            '//div[@class="content"]//div[@class="f0"]/div[1]/span[2]/text()').extract()
        item["电话"] = tel[0] if tel else '暂无电话信息'

        # emails = response.xpath(
        #     '//div[@class="content"]//div[@class="f0"]/div[2]/span[@class="email"]/text()').extract()
        # item["邮箱"] = emails[0] if emails else '暂无邮箱信息'

        address = response.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[5]/div[2]/div[2]/span[2]/@title').extract()
        item['地址'] = address[0] if address else '暂无地址信息'

        faren = response.xpath('//*[@id="_container_baseInfo"]/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[1]/a/text()').extract()
        item['法人'] =  faren[0] if faren else '暂无法人信息'


        staff_size = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()').extract()
        item['人员规模'] = staff_size[0] if staff_size else '暂无企业人数信息'

        buz_scope = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[2]/span/span/span[1]/text()').extract()
        item['经营范围'] = buz_scope[0] if buz_scope else '暂无企业经营范围信息'

        #工商注册号
        item['工商注册号'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/text()').extract_first()
        #组织机构代码
        item['组织机构代码'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]/text()').extract_first()
        #统一信用代码
        item['统一信用代码'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/text()').extract_first()
        #公司类型
        item['公司类型'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]/text()').extract_first()
        #纳税人识别号
        item['纳税人识别号'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()').extract_first()
        #行业
        item['行业'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()').extract_first()
        #参保人数
        item['参保人数'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/text()').extract_first()

        yield item

        #软件著作权
        # copyright = response.xpath('//div[@class="block-data"]/div[@id="_container_copyright"]/table/tbody/tr')
        # if copyright:
        #     item['软件著作权'] = []
        #     for cr in copyright:
        #         item29 = {}
        #         item29['序号'] = cr.xpath('.//td[1]/text()').extract_first()
        #         item29['批准日期'] = cr.xpath('.//td[2]/span/text()').extract_first()
        #         item29['软件全称'] = cr.xpath('.//td[3]/span/text()').extract_first()
        #         item29['软件简称'] = cr.xpath('.//td[4]/span/text()').extract_first()
        #         item29['登记号'] = cr.xpath('.//td[5]/span/text()').extract_first()
        #         item29['分类号'] = cr.xpath('.//td[6]/span/text()').extract_first()
        #         item29['版本号'] = cr.xpath('.//td[7]/span/text()').extract_first()
        #         item['软件著作权'].append(item29)
        # else:
        #     item['软件著作权'] = '暂无软件著作权信息'
        
        #可翻页字段
        # kefanyeziduan = response.xpath('//div/ul/@change-type').extract()
        # # if kefanyeziduan:
        # for fanye_i in kefanyeziduan:
        #     if fanye_i == 'jingpin':
        #         url1 = self.page_url1.format(fanye_i,self.page,self.company_name)
        #         yield scrapy.Request(url1, callback=self.parse_detailspage, meta={'item': item})
        #     else:
        #         url2 = self.page_url.format(fanye_i,self.page,company_id)
        #         yield scrapy.Request(url2, callback=self.parse_detailspage, meta={'item': item})
        # else:
        #     yield item

    # def parse_detailspage(self, response):
        # #获取并判断翻页的字段
        # search_ziduan=re.findall('pagination/(.*?).xhtml',response.url)[0]
        # if search_ziduan == 'recruit':
        # #招聘信息
        #     zhaopin = response.xpath('//tbody/tr')
        #     if zhaopin:
        #         item['招聘信息'] = []
        #         for zp in zhaopin:
        #             item1 = {}
        #             item1['序号'] = zp.xpath('.//td[1]/text()').extract_first()
        #             item1['发布时间'] = zp.xpath('.//td[2]/text()').extract_first()
        #             item1['招聘岗位'] = zp.xpath('.//td[3]/text()').extract_first()
        #             item1['薪资'] = zp.xpath('.//td[4]/text()').extract_first()
        #             item1['工作经验'] = zp.xpath('.//td[5]/text()').extract_first()
        #             item1['招聘人数'] = zp.xpath('.//td[6]/text()').extract_first()
        #             item1['所在城市'] = zp.xpath('.//td[7]/text()').extract_first()
        #             item['招聘信息'].append(item1)
        #     else:
        #         item['招聘信息'] = '暂无招聘信息'
        #     # yield item

        # elif search_ziduan == 'jingpin':
        # #竞品信息
        #     jingpin = response.xpath('//tbody/tr')
        #     if jingpin:
        #         item['竞品信息'] = []
        #         for jp in jingpin:
        #             item2 = {}
        #             item2['序号'] = jp.xpath('.//td[1]/text()').extract_first()
        #             item2['产品'] = jp.xpath('.//td[2]//a[@class="link-click"]/text()').extract_first()
        #             item2['地区'] = jp.xpath('.//td[3]/text()').extract_first()
        #             item2['当前轮次'] = jp.xpath('.//td[4]/text()').extract_first()
        #             item2['行业'] = jp.xpath('.//td[5]//a[@class="link-click"]/text()').extract_first()
        #             item2['业务'] = jp.xpath('.//td[6]/text()').extract_first()
        #             item2['成立时间'] = jp.xpath('td[7]/text()').extract_first()
        #             item2['估值'] = jp.xpath('td[8]/text()').extract_first()
        #             item['竞品信息'].append(item2)
        #     else:
        #         item['竞品信息'] = '暂无竞品信息'

        #     # yield item
        # elif search_ziduan == 'changeinfo':
        #     changeinfo = response.xpath('//tbody/tr')
        #     if changeinfo:
        #         item['变更记录'] = []
        #         for ci in changeinfo:
        #             item3 = {}
        #             item3['序号'] = ci.xpath('.//td[1]/text()').extract_first()
        #             item3['变更时间'] = ci.xpath('.//td[2]/text()').extract_first()
        #             item3['变更项目'] = ci.xpath('.//td[3]/text()').extract_first()
        #             item3['变更前'] = ci.xpath('.//td[4]//text()').extract_first()
        #             item3['变更后'] = ci.xpath('.//td[5]//text()').extract_first()
        #             item['变更记录'].append(item3)
        #     else:
        #         item['变更记录'] = '暂无变更记录信息'
        
        # # elif search_ziduan == 'copyright':
        # else:
        #     copyright = response.xpath('//tbody/tr')
        #     if copyright:
        #         item['软件著作权'] = []
        #         for cr in copyright:
        #             item4 = {}
        #             item4['序号'] = cr.xpath('.//td[1]/text()').extract_first()
        #             item4['批准日期'] = cr.xpath('.//td[2]/span/text()').extract_first()
        #             item4['软件全称'] = cr.xpath('.//td[3]/span/text()').extract_first()
        #             item4['软件简称'] = cr.xpath('.//td[4]/span/text()').extract_first()
        #             item4['登记号'] = cr.xpath('.//td[5]/span/text()').extract_first()
        #             item4['分类号'] = cr.xpath('.//td[6]/span/text()').extract_first()
        #             item4['版本号'] = cr.xpath('.//td[7]/span/text()').extract_first()
        #             item['软件著作权'].append(item4)
        #     else:
        #         item['软件著作权'] = '暂无软件著作权信息'

        yield item



