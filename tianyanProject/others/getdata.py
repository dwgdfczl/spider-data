# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import requests
import time
import math
from ..items import CompanycodeItem
from ..settings import COOKIES, DEFAULT_REQUEST_HEADERS, headers2
from scrapy.spiders import CrawlSpider

class Myspider(scrapy.Spider):
    name = 'company'
    allowed_domains = ["www.tianyancha.com"]
    start_urls = ['http://www.tianyancha.com']
    company_name = ''
    # new_url = None
    # url = None

    def start_requests(self):
        f = open('companylist', 'r')
        for obj in f:
            DEFAULT_REQUEST_HEADERS["Referer"] = "https://www.tianyancha.com/"
            item = CompanycodeItem()
            self.company_name = obj
            self.url = "http://www.tianyancha.com/search?key=%s" % (urllib.parse.quote(self.company_name))
            yield scrapy.Request(self.url, cookies=COOKIES, meta={'item': item},  callback=self.parse_page)


    def parse_page(self,response):
        headers2["Referer"] = self.url

        item = response.meta['item']

        # # item['公司名'] = self.company_name
        # # 公司注册时间
        # reg_time = response.xpath(
        #     '//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[3]/span/@title').extract()
        # item["注册时间"] = reg_time[0] if reg_time else ''

        # emails = response.xpath(
        #     '//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/span[2]/text()').extract()
        # item["邮箱"] = emails[0] if emails else ''

        # tel = response.xpath(
        #     '//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[1]/span[2]/text()').extract()
        # item["电话"] = tel[0] if tel else ''

        # company_status = response.xpath(
        #     '//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/text()').extract()
        # item["经营状态"] = company_status[0] if company_status else ''

        # reg_capital = response.xpath(
        #     '//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/span/text()').extract()
        # item["注册资本"] = reg_capital[0] if reg_capital else ''
        #获取公司详情页链接
        infos = response.xpath('//*[@id="web-content"]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/a/@href').extract_first()      
        if infos:
            DEFAULT_REQUEST_HEADERS["Referer"] = infos
            # item["公司在天眼查的url"] = infos
            yield scrapy.Request(url=infos, cookies=COOKIES, meta={'item': item}, callback=self.parse_info)
        else:
            item["公司在天眼查的url"] = '暂无该公司信息'
            yield item

    def parse_info(self, response):
        item = response.meta['item']
        data_page = response.xpath('//div[@class="block-data"]/div[@id="_container_patent"]//div[@class="company_pager"]/ul')
        if data_page:

            pagination = data_page.xpath('.//@class').extract_first()

            change_type = data_page.xpath('.//@change-type').extract_first()

            page_total = data_page.xpath('.//@page_total').extract_first()

        # #math.ceil(page_total/20)

            for i in range(1,20):
                # self.url1 = "https://www.tianyancha.com/%s/%s.xhtml?ps=10&pn=%s&name=%s" %(pagination, change_type, i,urllib.parse.quote(self.company_name))
                self.url1 = "https://www.tianyancha.com/%s/%s.xhtml?ps=10&pn=%s&id=22822" %(pagination, change_type, i)
                yield scrapy.Request(self.url1, cookies=COOKIES, meta={'item': item},  callback=self.parse_page1)

        # else:
        # yield scrapy.Request(self.url, cookies=COOKIES, meta={'item': item},  callback=self.parse_page1)


        # else:
        #     self.url = DEFAULT_REQUEST_HEADERS["Referer"]
        #     yield scrapy.Request(url=self.url, cookies=COOKIES, meta={'item': item}, callback=self.parse_page1)




        # data_page = response.xpath('//div[@class="company_pager"]/ul')
        
       
        # self.url = "https://www.tianyancha.com/pagination/jingpin.xhtml?"+ urllib.parse.urlencode(data)
        # yield scrapy.FormRequest(self.url, cookies=COOKIES, meta={'item': item}, formdata = data, callback=self.parse_page1)
    def parse_page1(self, response):
        item = response.meta['item']

        # name = response.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[1]/h1/text()').extract()
        # item['公司名'] = name[0] if name else '暂无公司名称信息'

        # tel = response.xpath(
        #     '//div[@class="content"]//div[@class="f0"]/div[1]/span[2]/text()').extract()
        # item["电话"] = tel[0] if tel else '暂无电话信息'

        # emails = response.xpath(
        #     '//div[@class="content"]//div[@class="f0"]/div[2]/span[@class="email"]/text()').extract()
        # item["邮箱"] = emails[0] if emails else '暂无邮箱信息'

        # address = response.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[5]/div[2]/div[2]/span[2]/@title').extract()
        # item['地址'] = address[0] if address else '暂无地址信息'

        # faren = response.xpath('//*[@id="_container_baseInfo"]/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[1]/a/text()').extract()
        # item['法人'] =  faren[0] if faren else '暂无法人信息'


        # staff_size = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()').extract()
        # item['人员规模'] = staff_size[0] if staff_size else '暂无企业人数信息'

        # buz_scope = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[2]/span/span/span[1]/text()').extract()
        # item['经营范围'] = buz_scope[0] if buz_scope else '暂无企业经营范围信息'

        # #工商注册号
        # item['工商注册号'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/text()').extract_first()
        # #组织机构代码
        # item['组织机构代码'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]/text()').extract_first()
        # #统一信用代码
        # item['统一信用代码'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/text()').extract_first()
        # #公司类型
        # item['公司类型'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]/text()').extract_first()
        # #纳税人识别号
        # item['纳税人识别号'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()').extract_first()
        # #行业
        # item['行业'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()').extract_first()
        # #参保人数
        # item['参保人数'] = response.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/text()').extract_first()

        # yield item
        
        #天眼风险
        # risk = response.xpath('//div[@class="block-data"]/div[2]/div[@class="eye-risk"]')
        # # item['自身风险'] = risk[0] if risk else '暂无企业风险信息'
        # item['天眼风险'] = []
        # for ri in risk:
        #     item = {}
        #     item['自身风险'] = ri.xpath('.//div[@class="self-risk "]/div[1]/span/text()').extract_first()
        #     item['周边风险'] = ri.xpath('').extract_first()
        #     item['预警提醒'] = ri.xpath('').extract_first()

        # #主要成员
        # leading_member = response.xpath('//div[@class="block-data"]/div[@id="_container_staff"]/div/table/tbody/tr')
        # if leading_member:
        #     item['主要成员'] = []
        #     for lead_m in leading_member:
        #         item0 = {}
        #         item0['序号'] = lead_m.xpath('.//td[1]/text()').extract_first()
        #         item0['主要人员'] = lead_m.xpath('.//td[2]/div/a[1]/text()').extract_first()
        #         item0['职位'] = lead_m.xpath('.//td[3]/span/text()').extract_first()
        #         item['主要成员'].append(item0)
        # else:
        #     item['主要成员'] = '暂无主要成员信息'

        # #股东信息
        # shareholder = response.xpath('//div[@class="block-data"]/div[@id="_container_holder"]/table[@class="table"]/tbody/tr')
        # if shareholder:
        #     item['股东团队'] = []
        #     for sh in shareholder:
        #         item1 = {}
        #         item1['股东'] = sh.xpath('.//td/div[@class="text-image-human"]/div[2]/a/text()').extract_first()
        #         item1['公司数量'] = sh.xpath('.//td[2]/div/div[3]/span/a/text()').extract_first()
        #         item1['出资比例'] = sh.xpath('.//td[3]/div/div/span/text()').extract_first()
        #         item1['认缴出资'] = sh.xpath('.//td[4]/div/span/text()').extract_first()
        #         item1['出资时间'] = sh.xpath('.//td[5]/div/span/text()').extract_first()
        #         item['股东团队'].append(item1)
        # else:
        #     item['股东团队'] = '暂无股东团队信息'

        # #对外投资
        # outinvestment = response.xpath('//div[@class="block-data"]/div[@id="_container_invest"]/table/tbody/tr')
        # if outinvestment:
        #     item['对外投资'] = []
        #     for outinv in outinvestment:
        #         item2 = {}
        #         item2['被投资公司名称'] = outinv.xpath('.//td[2]/a/text()').extract_first()
        #         item2['被投资法定代表人'] = outinv.xpath('.//td[3]/span/a/text()').extract_first()
        #         item2['注册资本'] = outinv.xpath('.//td[4]/span/text()').extract_first()
        #         item2['投资占比'] = outinv.xpath('.//td[5]/span/text()').extract_first()
        #         item2['注册时间'] = outinv.xpath('.//td[6]/span/text()').extract_first()
        #         item2['状态'] = outinv.xpath('.//td[7]/span/text()').extract_first()
        #         item['对外投资'].append(item2)
        # else:
        #     item['对外投资'] = '暂无对外投资信息'

        # #最终受益人
        # shouyiren = response.xpath('//div[@class="block-data"]/div[@id="_container_humanholding"]/table')
        # if shouyiren:
        #     item['最终受益人'] = []
        #     for syr in shouyiren:
        #         item3 = {}
        #         item3['最终受益人名称'] = syr.xpath('.//tbody/tr/td[2]/span/a[@class="link-click"]/text()').extract_first()
        #         item3['持股比例'] = syr.xpath('.//tbody/tr/td[3]/span[@class="num-shareholding-ratio"]/text()').extract_first()
        #         item3['股权链'] = syr.xpath('.//tbody/tr/td[4]/div[@class="chain-equity"]/div/b/text()').extract_first()
        #         item['最终受益人'].append(item3)
        # else:
        #     item['最终受益人'] = '暂无最终受益人信息'

        # # 实际控制权
        # # realHolding = response.xpath('//div/div[@id="_container_companyholding"]/table[@class="table"]/tbody/tr')
        # # if realHolding:
        # #     item['实际控制权'] = []
        # #     for rh in realHolding:
        # #         item4 = {}
        # #         item4['序号'] = rh.xpath('.').extract_first()   
        # #         item4['控股企业名称'] = rh.xpath('.').extract_first()   
        # #         item4['投资比例'] = rh.xpath('.').extract_first()   
        # #         item4['股权链'] = rh.xpath('.').extract_first()
        # #         item['实际控制权'].append(item4)
        # # else:
        # #     item['实际控制权'] = '暂无实际控股权信息'

        # # 变更记录
        # change = response.xpath('//div[@class="block-data"]/div[@id="_container_changeinfo"]/table/tbody/tr')
        # if change:
        #     item['变更记录'] = []
        #     for cha in change:
        #         item5 = {}
        #         item5['序号'] = cha.xpath('.//td[1]/text()').extract_first()
        #         item5['变更时间'] = cha.xpath('.//td[2]/text()').extract_first()
        #         item5['变更项目'] = cha.xpath('.//td[3]/text()').extract_first()
        #         # item5['变更前'] = cha.xpath('.//td[4]/div/text()').extract_first()
        #         change_before = cha.xpath('.//td[4]/div')
        #         item5['变更前'] = change_before.xpath('string(.)').extract_first()
        #         # item5['变更后'] = cha.xpath('.//td[5]/div//text()').extract_first()
        #         change_after = cha.xpath('.//td[5]/div')
        #         item5['变更后'] = change_after.xpath('string(.)').extract_first()
        #         item['变更记录'].append(item5)
        # else:
        #     item['变更记录'] = '暂无变更记录'

        # #公司年报
        # report = response.xpath('//div[@class="data-content"]/div[@class="report-item-list"]/div')
        # if report:
        #     item['公司年报'] = []
        #     for rep in report:
        #         item6 = {}
        #         item6['时间'] = rep.xpath('.//span[2]/text()').extract_first()
        #         item6['详情地址'] = rep.xpath('.//a/@href').extract_first()
        #         item['公司年报'].append(item6)
        # else:
        #     item['公司年报'] = '暂无公司年报信息'

        # #分支机构
        # branch = response.xpath('//div[@class="block-data"]/div[@id="_container_branch"]/table[@class="table"]/tbody/tr')
        # if branch:
        #     item['分支机构'] = []
        #     for bra in branch:
        #         item7 = {}
        #         item7['序号'] = bra.xpath('.//td[1]/text()').extract_first()
        #         item7['企业名称'] = bra.xpath('.//td[2]//a/text()').extract_first()
        #         item7['负责人'] = bra.xpath('.//td[3]/span/text()').extract_first()
        #         item7['注册时间'] = bra.xpath('.//td[4]/span/text()').extract_first()
        #         item7['状态'] = bra.xpath('.//td[5]/span/text()').extract_first()
        #         item['分支机构'].append(item7)
        # else:
        #     item['分支机构'] = '暂无分支机构信息'

        # #开庭公告
        # announcement = response.xpath('//div[@class="block-data"]/div[@id="_container_announcementcourt"]/table[@class="table"]/tbody/tr')
        # if announcement:
        #     item['开庭公告'] = []
        #     for anno in announcement:
        #         item8 = {}
        #         item8['序号'] = anno.xpath('.//td[1]/text()').extract_first()
        #         item8['开庭时间'] = anno.xpath('.//td[2]/text()').extract_first()
        #         item8['案由'] = anno.xpath('.//td[3]/span/text()').extract_first()
        #         # item8['原告'] = anno.xpath('.//td[4]/div/a/text()').extract_first()
        #         item8['原告'] = anno.xpath('.//td[4]//text()').extract_first()
        #         # item8['被告'] = anno.xpath('.//td[5]//text()').extract_first()
        #         beigao = anno.xpath('.//td[5]')
        #         item8['被告'] = beigao.xpath('string(.)').extract_first()
        #         item['开庭公告'].append(item8)
        # else:
        #     item['开庭公告'] = '暂无开庭公告信息'

        # #法律诉讼
        # lawrisk = response.xpath('//div[@class="block-data"]/div[@id="_container_lawsuit"]/table/tbody/tr')
        # if lawrisk:
        #     item['法律诉讼'] = []
        #     for lawr in lawrisk:
        #         item9 = {}
        #         item9['序号'] = lawr.xpath('.//td[1]/text()').extract_first()
        #         item9['日期'] = lawr.xpath('.//td[2]/span/text()').extract_first()
        #         item9['裁判文书'] = lawr.xpath('.//td[3]/a/@href').extract_first()
        #         item9['案由'] = lawr.xpath('.//td[4]/span/text()').extract_first()
        #         item9['上诉人'] = lawr.xpath('.//td[5]/div[1]/a/text()').extract_first()
        #         item9['被上诉人'] = lawr.xpath('.//td[5]/div[2]/a/text()').extract_first()
        #         item9['案号'] = lawr.xpath('.//td[6]/span/text()').extract_first()
        #         item['法律诉讼'].append(item9)
        # else:
        #     item['法律诉讼'] = '暂无法律诉讼信息'

        # #经营风险
        # #行政处罚【工商局】
        # gongshangju = response.xpath('//div[@id="_container_punish"]/table/tbody/tr')
        # if gongshangju:
        #     item['工商局处罚'] = []
        #     for gsj in gongshangju:
        #         item10 = {}
        #         item10['序号'] = gsj.xpath('.//td[1]/text()').extract_first()
        #         item10['决定日期'] = gsj.xpath('.//td[2]/text()').extract_first()
        #         item10['决定文书号'] = gsj.xpath('.//td[3]/text()').extract_first()
        #         item10['类型'] = gsj.xpath('.//td[4]/text()').extract_first()
        #         item10['决定机关'] = gsj.xpath('.//td[5]/text()').extract_first()
        #         item10['详细信息'] = gsj.xpath('.//td[6]/script/text()').extract_first()
        #         item['工商局处罚'].append(item10)
        # else:
        #     item['工商局处罚'] = '暂无工商局处罚'

        # #行政处罚【信用中国】
        # xinyongzhongguo = response.xpath('//div[@id="_container_punishCreditchina"]/table/tbody/tr')
        # if xinyongzhongguo:
        #     item['信用中国'] = []
        #     for xyzg in xinyongzhongguo:
        #         item11 = {}
        #         item11['序号'] = xyzg.xpath('.//td[1]/text()').extract_first()
        #         item11['决定日期'] = xyzg.xpath('.//td[2]/text()').extract_first()
        #         item11['决定文书号'] = xyzg.xpath('.//td[3]/text()').extract_first()
        #         item11['处罚名称'] = xyzg.xpath('.//td[4]/text()').extract_first()
        #         item11['处罚机关'] = xyzg.xpath('.//td[5]/text()').extract_first()
        #         item['信用中国'].append(item11)
        # else:
        #     item['信用中国'] = '暂无信用中国处罚信息'

        # #股权出质
        # guquanchuzhi = response.xpath('//div[@class="block-data"]/div[@id="_container_equity"]/table/tbody/tr')
        # if guquanchuzhi:
        #     item['股权出质'] = []
        #     for gqcz in guquanchuzhi:
        #         item12 = {}
        #         item12['序号'] = gqcz.xpath('.//td[1]/text()').extract_first()
        #         item12['公告时间'] = gqcz.xpath('.//td[2]/text()').extract_first()
        #         item12['登记编号'] = gqcz.xpath('.//td[3]/text()').extract_first()
        #         item12['出质人'] = gqcz.xpath('.//td[4]/a/text()').extract_first()
        #         item12['质权人'] = gqcz.xpath('.//td[5]/a/text()').extract_first()
        #         item12['状态'] = gqcz.xpath('.//td[6]/text()').extract_first()
        #         item['股权出质'].append(item12)
        # else:
        #     item['股权出质'] = '暂无股权出质信息'

        # #融资历史
        # rongzhi = response.xpath('//div[@class="block-data"]/div[@id="_container_rongzi"]/table/tbody/tr')
        # if rongzhi:
        #     item['融资历史'] = []
        #     for rz in rongzhi:
        #         item13 = {}
        #         item13['序号'] = rz.xpath('.//td[1]/text()').extract_first()
        #         item13['时间'] = rz.xpath('.//td[2]/text()').extract_first()
        #         item13['轮次'] = rz.xpath('.//td[3]/text()').extract_first()
        #         item13['估值'] = rz.xpath('.//td[4]/text()').extract_first()
        #         item13['金额'] = rz.xpath('.//td[5]/text()').extract_first()
        #         item13['比例'] = rz.xpath('.//td[6]/text()').extract_first()
        #         item13['投资方'] = rz.xpath('.//td[7]/div//text()').extract_first()
        #         item13['新闻来源'] = rz.xpath('.//td[8]/span/text()').extract_first()
        #         item['融资历史'].append(item)
        # else:
        #     item['融资历史'] = '暂无融资历史信息'

        # #核心团队
        # keymember = response.xpath('//div[@class="block-data"]/div[@id="_container_teamMember"]/div/div')
        # if keymember:
        #     item['核心团队'] = []
        #     for km in keymember:
        #         item14 = {}
        #         item14['姓名'] = km.xpath('.//div[@class="logo -w64"]/img/@alt').extract_first()
        #         item14['职位'] = km.xpath('.//div[@class="right"]/div/text()').extract_first()
        #         jieshao = km.xpath('.//div[@class="right"]//p')
        #         item14['介绍'] = jieshao.xpath('string(.)').extract_first()
        #         item['核心团队'].append(item14)
        # else:
        #     item['核心团队'] = '暂无核心团队信息'

        # #企业业务
        # firmProduct = response.xpath('//div[@class="block-data"]/div[@id="_container_firmProduct"]/div/a')
        # if firmProduct:
        #     item['企业业务'] = []
        #     for fp in firmProduct:
        #         item15 = {}
        #         item15['名称'] = fp.xpath('.//div[2]/div[@class="title"]/text()').extract_first()
        #         item15['介绍'] = fp.xpath('.//div[2]/div/@title').extract_first()
        #         item15['类别'] = fp.xpath('.//div[2]/div[3]/text()').extract_first()
        #         item['企业业务'].append(item15)
        # else:
        #     item15['企业业务'] = '暂无企业业务信息'

        # #投资事件
        # touzi = response.xpath('//div[@class="block-data"]/div[@id="_container_touzi"]/table/tbody/tr')
        # if touzi:
        #     item['投资事件'] = []
        #     for tz in touzi:
        #         item16 = {}
        #         item16['序号'] = tz.xpath('.//td[1]/text()').extract_first()
        #         item16['时间'] = tz.xpath('.//td[2]/text()').extract_first()
        #         item16['轮次'] = tz.xpath('.//td[3]/text()').extract_first()
        #         item16['金额'] = tz.xpath('.//td[4]/text()').extract_first()
        #         # item16['投资方'] = tz.xpath('.///td[5]/div').extract_first()
        #         touzifang = tz.xpath('.//td[5]')
        #         item16['投资方'] = touzifang.xpath('string(.)').extract_first()
        #         item16['产品'] = tz.xpath('.//td[6]//a/text()').extract_first()
        #         item16['地区'] = tz.xpath('.//td[7]/text()').extract_first()
        #         item16['行业'] = tz.xpath('.//td[8]/a/text()').extract_first()
        #         item16['业务'] = tz.xpath('.//td[9]/text()').extract_first()
        #         item['投资事件'].append(item16)
        # else:
        #     item['投资事件'] = '暂无投资事件信息'

        # #竞品信息
        # data_page = response.xpath('//div[@class="block-data"]/div[@id="_container_jingpin"]//div[@class="company_pager"]/ul')
        # if data_page:
        # jingpin = response.xpath('//div[@class="block-data"]/div[@id="_container_jingpin"]/div/table/tbody/tr')
        # if jingpin:
        #     item['竞品信息'] = []
        #     for jp in jingpin:
        #         item17 = {}
        #         item17['序号'] = jp.xpath('.//td[1]/text()').extract_first()
        #         item17['产品'] = jp.xpath('.//td[2]//a/text()').extract_first()
        #         item17['地区'] = jp.xpath('.//td[3]/text()').extract_first()
        #         item17['当前轮次'] = jp.xpath('.//td[4]/text()').extract_first()
        #         item17['行业'] = jp.xpath('.//td[5]/a/text()').extract_first()
        #         item17['业务'] = jp.xpath('.//td[6]/text()').extract_first()
        #         item17['成立时间'] = jp.xpath('.//td[7]/text()').extract_first()
        #         item17['估值'] = jp.xpath('.//td[8]/text()').extract_first()
        #         item['竞品信息'].append(item17)
        # else:
        #     item['竞品信息'] = '暂无竞品信息'

        # jingpin = response.xpath('//div/table/tbody/tr')
        # if jingpin:
        #     item['竞品信息'] = []
        #     for jp in jingpin:
        #         item17 = {}
        #         item17['序号'] = jp.xpath('.//td[1]/text()').extract_first()
        #         item17['产品'] = jp.xpath('.//td[2]//a/text()').extract_first()
        #         item17['地区'] = jp.xpath('.//td[3]/text()').extract_first()
        #         item17['当前轮次'] = jp.xpath('.//td[4]/text()').extract_first()
        #         item17['行业'] = jp.xpath('.//td[5]/a/text()').extract_first()
        #         item17['业务'] = jp.xpath('.//td[6]/text()').extract_first()
        #         item17['成立时间'] = jp.xpath('.//td[7]/text()').extract_first()
        #         item17['估值'] = jp.xpath('.//td[8]/text()').extract_first()
        #         item['竞品信息'].append(item17)
        # else:
        #     item['竞品信息'] = '暂无竞品信息'

        # yield item

        # #招聘信息
        # zhaopin = response.xpath('//div[@class="block-data"]/div[@id="_container_recruit"]/table/tbody/tr')
        # if zhaopin:
        #     item['招聘信息'] = []
        #     for zp in zhaopin:
        #         item18 = {}
        #         item18['序号'] = zp.xpath('.//td[1]/text()').extract_first()
        #         item18['发布时间'] = zp.xpath('.//td[2]/text()').extract_first()
        #         item18['招聘岗位'] = zp.xpath('.//td[3]/text()').extract_first()
        #         item18['薪资'] = zp.xpath('.//td[4]/text()').extract_first()
        #         item18['工作经验'] = zp.xpath('.//td[5]/text()').extract_first()
        #         item18['招聘人数'] = zp.xpath('.//td[6]/text()').extract_first()
        #         item18['所在城市'] = zp.xpath('.//td[7]/text()').extract_first()
        #         item['招聘信息'].append(item18)
        # else:
        #     item['招聘信息'] = '暂无招聘信息'

        # #行政许可【工商局】
        # gsj_licensing = response.xpath('//div[@class="block-data"]/div[@id="_container_licensing"]/table/tbody/tr')
        # if gsj_licensing:
        #     item['行政许可_工商局'] = []
        #     for li in gsj_licensing:
        #         item19 = {}
        #         item19['序号'] = li.xpath('.//td[1]/text()').extract_first()
        #         item19['许可书文编号'] = li.xpath('.//td[2]/text()').extract_first()
        #         item19['许可文件名称'] = li.xpath('.//td[3]/text()').extract_first()
        #         item19['有效期自'] = li.xpath('.//td[4]/text()').extract_first()
        #         item19['有效期至'] = li.xpath('.//td[5]/text()').extract_first()
        #         item19['许可机关'] = li.xpath('.//td[6]/text()').extract_first()
        #         item19['内容'] = li.xpath('.//td[7]/text()').extract_first()
        #         item['行政许可_工商局'].append(item19)
        # else:
        #     item['行政许可_工商局'] = '暂无行政许可信息'

        # #行政许可【信用中国】
        # xyzg_licensing = response.xpath('//div[@class="block-data"]/div[@id="_container_licensingXyzg"]/table/tbody/tr')
        # if xyzg_licensing:
        #     item['行政许可_信用中国'] = []
        #     for xyzg in xyzg_licensing:
        #         item20 = {}
        #         item20['序号'] = xyzg.xpath('.//td[1]/text()').extract_first()
        #         item20['行政许可文书号'] = xyzg.xpath('.//td[2]/text()').extract_first()
        #         item20['许可决定机关'] = xyzg.xpath('.//td[3]/text()').extract_first()
        #         item20['许可决定日期'] = xyzg.xpath('.//td[4]/text()').extract_first()
        #         item['行政许可_信用中国'].append(item20)
        # else:
        #     item['行政许可_信用中国'] = '暂无行政许可_信用中国信息'

        # #税务评级
        # taxcredit = response.xpath('//div[@class="block-data"]/div[@id="_container_taxcredit"]/table/tbody/tr')
        # if taxcredit:
        #     item['税务评级'] = []
        #     for tax in taxcredit:
        #         item21 = {}
        #         item21['序号'] = tax.xpath('.//td[1]/text()').extract_first()
        #         item21['年份'] = tax.xpath('.//td[2]/text()').extract_first()
        #         item21['纳税评级'] = tax.xpath('.//td[3]/text()').extract_first()
        #         item21['类型'] = tax.xpath('.//td[4]/text()').extract_first()
        #         item21['纳税人识别号'] = tax.xpath('.//td[5]/text()').extract_first()
        #         item21['评级单位'] = tax.xpath('.//td[6]/text()').extract_first()
        #         item['税务评级'].append(item21)
        # else:
        #     item['税务评级'] = '暂无税务评级信息'

        # #抽查检查
        # randomcheck = response.xpath('//div[@class="block-data"]/div[@id="_container_check"]/div/table/tbody/tr')
        # if randomcheck:
        #     item['抽查检查'] = []
        #     for ranche in randomcheck:
        #         item22 = {}
        #         item22['序号'] = ranche.xpath('.//td[1]/text()').extract_first()
        #         item22['日期'] = ranche.xpath('.//td[2]/text()').extract_first()
        #         item22['类型'] = ranche.xpath('.//td[3]/text()').extract_first()
        #         item22['结果'] = ranche.xpath('.//td[4]/text()').extract_first()
        #         item22['检查实施单位'] = ranche.xpath('.//td[5]/text()').extract_first()
        #         item['抽查检查'].append('item22')
        # else:
        #     item['抽查检查'] = '暂无抽查检查信息'

        # #资质证书
        # certificate = response.xpath('//div[@class="block-data"]/div[@id="_container_certificate"]/table/tbody/tr')
        # if certificate:
        #     item['资质证书'] = []
        #     for cert in certificate:
        #         item23 = {}
        #         item23['序号'] = cert.xpath('.//td[1]/text()').extract_first()
        #         item23['证书类型'] = cert.xpath('.//td[2]/span/text()').extract_first()
        #         item23['证书编号'] = cert.xpath('.//td[3]/span/text()').extract_first()
        #         item23['发证日期'] = cert.xpath('.//td[4]/span/text()').extract_first()
        #         item23['截止日期'] = cert.xpath('.//td[5]/span/text()').extract_first()
        #         item['资质证书'].append(item23)
        # else:
        #     item['资质证书'] = '暂无资质证书信息'

        # #招投标
        # bid = response.xpath('//div[@class="block-data"]/div[@id="_container_bid"]/table/tbody/tr')
        # if bid:
        #     item['招投标'] = []
        #     for bi in bid:
        #         item24 = {}
        #         item24['序号'] = bi.xpath('.//td[1]/text()').extract_first()
        #         item24['发布时间'] = bi.xpath('.//td[2]/text()').extract_first()
        #         item24['标题'] = bi.xpath('.//td[3]/a/text()').extract_first()
        #         item24['招投标url'] = bi.xpath('.//td[3]/a/@href').extract_first()
        #         item24['采购人'] = bi.xpath('.//td[4]/text()').extract_first()
        #         item['招投标'].append(item24)
        # else:
        #     item['招投标'] = '暂无招投标信息'

        # #产品信息
        # product = response.xpath('//div[@class="block-data"]/div[@id="_container_product"]/table/tbody/tr')
        # if product:
        #     item['产品信息'] = []
        #     for pro in product:
        #         item25 = {}
        #         item25['序号'] = pro.xpath('.//td[1]/text()').extract_first()
        #         item25['产品名称'] = pro.xpath('.//td[2]//span/text()').extract_first()
        #         item25['产品简称'] = pro.xpath('.//td[3]/span/text()').extract_first()
        #         item25['产品分类'] = pro.xpath('.//td[4]/span/text()').extract_first()
        #         item25['领域'] = pro.xpath('.//td[5]/span/text()').extract_first()
        #         item25['详情url'] = pro.xpath('.//td[6]/a/@href').extract_first()
        #         item['产品信息'].append(item25)
        # else:
        #     item['产品信息'] = '暂无产品信息'

        # #微信公众号
        # wechat = response.xpath('//div[@class="block-data"]/div[@id="_container_wechat"]/div/div')
        # if wechat:
        #     item['微信公众号'] = []
        #     for we in wechat:
        #         item26 = {}
        #         item26['名称'] = we.xpath('.//div[2]/div[1]/text()').extract_first()
        #         item26['微信号'] = we.xpath('.//div[2]/div[2]/span[2]/text()').extract_first()
        #         # item26['功能介绍'] = we.xpath('.//div/div[3]/span[2]/text()').extract_first()
        #         gongneng = we.xpath('.//div[@class="content"]//script/text()').extract_first()
        #         item26['功能介绍'] = eval(gongneng)['recommend']
        #         item['微信公众号'].append(item26)
        # else:
        #     item['微信公众号'] = '暂无微信公众号信息'



        # #商标信息
        # shangbiao = response.xpath('//div[@id="_container_tmInfo"]/div[@class="data-content"]/table/tbody/tr')
        # if shangbiao:
        #     item['商标信息'] = []
        #     for sb in shangbiao:
        #         item27['序号'] = sb.xpath('.//td[1]/text()').extract_first()
        #         item27['申请日期'] = sb.xpath('.//td[2]/span/text()').extract_first()
        #         item27['商标'] = sb.xpath('.//td[3]//img/@src').extract_first()
        #         item27['商标名称'] = sb.xpath('.//td[4]/span/text()').extract_first()
        #         item27['注册号'] = sb.xpath('.//td/span/text()').extract_first()
        #         item27['类别'] = sb.xpath('.//td[5]/span/text()').extract_first()
        #         item27['流程状态'] = sb.xpath('.//td[6]/span/text()').extract_first()
        #         item['商标信息'].append(item27)
        # else:
        #     item['商标信息'] = '暂无商标信息'

        #专利信息
        # patent = response.xpath('//div[@class="block-data"]/div[@id="_container_patent"]/table/tbody/tr')
        # if patent:
        #     item['专利信息'] = []
        #     for pa in patent:
        #         item28 = {}
        #         item28['序号'] = pa.xpath('.//td[1]/text()').extract_first()
        #         item28['申请公布日'] = pa.xpath('.//td[2]/span/text()').extract_first()
        #         item28['专利名称'] = pa.xpath('.//td[3]/span/text()').extract_first()
        #         item28['申请号'] = pa.xpath('.//td[4]/span/text()').extract_first()
        #         item28['申请公布号'] = pa.xpath('.//td[5]/span/text()').extract_first()
        #         item28['专利类型'] = pa.xpath('.//td[6]/span/text()').extract_first()
        #         item28['专利详情url'] = pa.xpath('.//td[7]/a/@href').extract_first()
        #         item['专利信息'].append(item28)
        # else:
        #     item['专利信息'] = '暂无专利信息'

        patent = response.xpath('//tbody/tr')
        if patent:
            item['专利信息'] = []
            for pa in patent:
                item28 = {}
                item28['序号'] = pa.xpath('.//td[1]/text()').extract_first()
                item28['申请公布日'] = pa.xpath('.//td[2]/span/text()').extract_first()
                item28['专利名称'] = pa.xpath('.//td[3]/span/text()').extract_first()
                item28['申请号'] = pa.xpath('.//td[4]/span/text()').extract_first()
                item28['申请公布号'] = pa.xpath('.//td[5]/span/text()').extract_first()
                item28['专利类型'] = pa.xpath('.//td[6]/span/text()').extract_first()
                # item28['专利详情url'] = pa.xpath('.//td[7]/a/@href').extract_first()
                item['专利信息'].append(item28)
        else:
            item['专利信息'] = '暂无专利信息'

        yield item

        # #软件著作权
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

        # #作品著作权
        # copyrightWorks = response.xpath('//div[@class="block-data"]/div[@id="_container_copyrightWorks"]/table/tbody/tr')
        # if copyrightWorks:
        #     item['作品著作权'] = []
        #     for crw in copyrightWorks:
        #         item30 = {}
        #         item30['序号'] = crw.xpath('.//td[1]/text()').extract_first()
        #         item30['作品名称'] = crw.xpath('.//td[2]/span/text()').extract_first()
        #         item30['登记号'] = crw.xpath('.//td[3]/span/text()').extract_first()
        #         item30['类别'] = crw.xpath('.//td[4]/span/text()').extract_first()
        #         item30['创作完成日期'] = crw.xpath('.//td[5]/span/text()').extract_first()
        #         item30['登记日期'] = crw.xpath('.//td[6]/span/text()').extract_first()
        #         item30['首次发布日期'] = crw.xpath('.//td[7]/span/text()').extract_first()
        #         item['作品著作权'].append(item30)
        # else:
        #     item['作品著作权'] = '暂无作品著作权信息'

        # #网站备案
        # ICP = response.xpath('//div[@class="block-data"]/div[@id="_container_icp"]/table/tbody/tr')
        # if ICP:
        #     item['网站备案'] = []
        #     for icp in ICP:
        #         item31 = {}
        #         item31['序号'] = icp.xpath('.//td[1]/text()').extract_first()
        #         item31['审核时间'] = icp.xpath('.//td[2]/span/text()').extract_first()
        #         item31['网站名称'] = icp.xpath('.//td[3]/span/text()').extract_first()
        #         wangzhanshouye = icp.xpath('.//td[4]')
        #         item31['网站首页'] = wangzhanshouye.xpath('string(.)').extract_first()
        #         item31['域名'] = icp.xpath('.//td[5]/text()').extract_first()
        #         item31['备案号'] = icp.xpath('.//td[6]/span/text()').extract_first()
        #         item31['状态'] = icp.xpath('.//td[7]/span/text()').extract_first()
        #         item31['单位性质'] = icp.xpath('.//td[8]/span/text()').extract_first()
        #         item['网站备案'].append(item31)
        # else:
        #     item['网站备案'] = '暂无网站备案信息'



        # #历史工商信息
        # #历史主要成员
        # # lishigongshang = response.xpath('//div[@class="block-data"]/div[@id="_container_pastICCount"]/table/tbody/tr')
        # # if lishigongshang:
        # #     item['历史工商信息'] = []
        # #     for lsgs in lishigongshang:
        # #         item32 = {}
        # #         item32['时间'] = lsgs.xpath('.//td[@class="date-col"]/text()').extract_first()
        # #         content = lsgs.xpath('.//td/a[@class="link-click"]/text()')
        # #         if content:
        # #             item32['内容'] = content.extract_first()
        # #         else:
        # #             content = lsgs.xpath('.//td[@class="left-col"]/text()')
        # #             item32['内容'] = content.extract_first()
        # #         else:
        # #             item32['内容'] = lsgs.xpath('.//td//span[@class="js-full-container hidden"]/text()').extract_first()
        # #         item['历史工商信息'].append(item32)
        # # else:
        # #     item['历史工商信息'] = '暂无历史工商信息'

        # #历史股东
        # lishigudong = response.xpath('//div[@class="block-data"]/div[@id="_container_pastHolderCount"]/table/tbody/tr')
        # if lishigudong:
        #     item['历史股东'] = []
        #     for lsgd in lishigudong:
        #         item33 = {}
        #         item33['序号'] = lsgd.xpath('.//td[1]/text()').extract_first()
        #         item33['股东'] = lsgd.xpath('.//td[2]//a/text()').extract_first()
        #         item33['出资比例'] = lsgd.xpath('.//td[3]//span/text()').extract_first()
        #         item33['认缴出资'] = lsgd.xpath('.//td[4]//span/text()').extract_first()
        #         item['历史股东'].append(item33)
        # else:
        #     item['历史股东'] = '暂无历史股东信息'

        # #历史对外投资
        # lishiinverst = response.xpath('//div[@class="block-data"]/div[@id="_container_pastInverstCount"]/table/tbody/tr')
        # if lishiinverst:
        #     item['历史对外投资'] = []
        #     for lsi in lishiinverst:
        #         item34 = {}
        #         item34['序号'] = lsi.xpath('.//td[1]/text()').extract_first()
        #         item34['被投资公司名称'] = lsi.xpath('.//td[2]//a/text()').extract_first()
        #         item34['被投资法定代表人'] = lsi.xpath('.//td[3]//a/text()').extract_first()
        #         item34['注册资本'] = lsi.xpath('.//td[4]/text()').extract_first()
        #         item34['投资占比'] = lsi.xpath('.//td[5]/span/text()').extract_first()
        #         item34['注册时间'] = lsi.xpath('.//td[6]/text()').extract_first()
        #         item34['状态'] = lsi.xpath('.//td[7]/text()').extract_first()
        #         item['历史对外投资'].append(item34)
        # else:
        #     item['历史对外投资'] = '暂无历史对外投资信息'

        # #历史开庭公告
        # lishikaitinggg = response.xpath('//div[@class="block-data"]/div[@id="_container_pastAnnouncementCount"]/table/tbody/tr')
        # if lishikaitinggg:
        #     item['历史开庭公告'] = []
        #     for lishigg in lishikaitinggg:
        #         item35 = {}
        #         item35['序号'] = lishigg.xpath('.//td[1]/text()').extract_first()
        #         item35['开庭日期'] = lishigg.xpath('.//td[2]/text()').extract_first()
        #         item35['案由'] = lishigg.xpath('.//td[3]/span/text()').extract_first()
        #         item35['原告'] = lishigg.xpath('.//td[4]//text()').extract_first()
        #         lsbeigao = lishigg.xpath('.//td[5]')
        #         item35['被告'] = lsbeigao.xpath('string(.)').extract_first()
        #         item['历史开庭公告'].append(item35)
        # else:
        #     item['历史开庭公告'] = '暂无历史开庭公告信息'

        # #历史法律申诉
        # lishilawrisk = response.xpath('//div[@class="block-data"]/div[@id="_container_pastLawsuitCount"]//table/tbody/tr')
        # if lishilawrisk:
        #     item['历史法律申诉'] = []
        #     for lslawr in lishilawrisk:
        #         item36 = {}
        #         item36['序号'] = lslawr.xpath('.//td[1]/text()').extract_first()
        #         item36['日期'] = lslawr.xpath('.//td[2]/span/text()').extract_first()
        #         item36['裁判文书'] = lslawr.xpath('.//td[3]/a/@href').extract_first()
        #         item36['案由'] = lslawr.xpath('.//td[4]/span/text()').extract_first()
        #         item36['上诉人'] = lslawr.xpath('.//td[5]/div[1]/a/text()').extract_first()
        #         item36['被上诉人'] = lslawr.xpath('.//td[5]/div[2]/a/text()').extract_first()
        #         item36['案号'] = lslawr.xpath('.//td[6]/span/text()').extract_first()
        #         item['历史法律申诉'].append(item36)
        # else:
        #     item['历史法律申诉'] = '暂无历史法律诉讼信息'

        # #历史股权出质
        # lishiguquanchuzhi = response.xpath('//div[@class="block-data"]/div[@id="_container_pastEquityCount"]/table/tbody/tr')
        # if lishiguquanchuzhi:
        #     item['历史股权出质'] = []
        #     for lishigqcz in lishiguquanchuzhi:
        #         item37 = {}
        #         item37['序号'] = lishigqcz.xpath('.//td[1]/text()').extract_first()
        #         item37['公告时间'] = lishigqcz.xpath('.//td[2]/text()').extract_first()
        #         item37['登记编号'] = lishigqcz.xpath('.//td[3]/text()').extract_first()
        #         item37['出质人'] = lishigqcz.xpath('.//td[4]/a/text()').extract_first()
        #         item37['质权人'] = lishigqcz.xpath('.//td[5]/a/text()').extract_first()
        #         item37['状态'] = lishigqcz.xpath('.//td[6]/text()').extract_first()
        #         item['历史股权出质'].append(item37)
        # else:
        #     item['历史股权出质'] = '暂无历史股权出质信息'

        # #历史被执行人
        # lsbeizhixingren = response.xpath('//div[@class="block-data"]/div[@id="_container_pastZhixing"]//table/tbody/tr')
        # if lsbeizhixingren:
        #     item['历史被执行人'] = []
        #     for lsbzxr in lsbeizhixingren:
        #         item38 = {}
        #         item38['序号'] = lsbzxr.xpath('.//td[1]/text()').extract_first()
        #         item38['立案日期'] = lsbzxr.xpath('.//td[2]/text()').extract_first()
        #         item38['执行标的'] = lsbzxr.xpath('.//td[3]/text()').extract_first()
        #         item38['案号'] = lsbzxr.xpath('.//td[4]/text()').extract_first()
        #         item38['执行法院'] = lsbzxr.xpath('.//td[5]/text()').extract_first()
        #         item['历史被执行人'].append(item38)
        # else:
        #     item['历史被执行人'] = '暂无历史被执行人信息'

        # #历史工商局处罚
        # lishigongshangju = response.xpath('//div[@id="_container_pastPunishmentIC"]/table/tbody/tr')
        # if lishigongshangju:
        #     item['历史工商局处罚'] = []
        #     for lishigsj in lishigongshangju:
        #         item39 = {}
        #         item39['序号'] = lishigsj.xpath('.//td[1]/text()').extract_first()
        #         item39['决定日期'] = lishigsj.xpath('.//td[2]/text()').extract_first()
        #         item39['决定文书号'] = lishigsj.xpath('.//td[3]/text()').extract_first()
        #         item39['类型'] = lishigsj.xpath('.//td[4]/text()').extract_first()
        #         item39['决定机关'] = lishigsj.xpath('.//td[5]/text()').extract_first()
        #         item39['详细信息'] = lishigsj.xpath('.//td[6]/script/text()').extract_first()
        #         item['历史工商局处罚'].append(item39)
        # else:
        #     item['历史工商局处罚'] = '暂无历史工商局处罚'

        # #进出口信用
        # IandE = response.xpath('//div[@class="block-data"]/div[@id="_container_importAndExport"]/table/tbody/tr')
        # if IandE:
        #     item['进出口信用'] = []
        #     for ie in IandE:
        #         item40 = {}
        #         item40['注册海关'] = ie.xpath('.//td[1]/text()').extract_first()
        #         item40['海关编码'] = ie.xpath('.//td[2]/text()').extract_first()
        #         item40['经营类别'] = ie.xpath('.//td[3]/text()').extract_first()

        # #历史失信人信息
        # lsshixinren = response.xpath('//div[@class="block-data"]/div[@id="_container_pastDishonest"]/table/tbody/tr')
        # if lsshixinren:
        #     item['历史失信人信息'] = []
        #     for lssxr in lsshixinren:
        #         item41 = {}
        #         item41['序号'] = lsscr.xpath('.//td[1]/text()')
        #         item41['立案日期'] = lsscr.xpath('.//td[2]/span/text()')
        #         item41['案号'] = lsscr.xpath('.//td[3]/text()')
        #         item41['执行法院'] = lsscr.xpath('.//td[4]/text()')
        #         item41['执行法院'] = lsscr.xpath('.//td[4]/text()')
        #         item41['履行状态'] = lsscr.xpath('.//td[5]/text()')
        #         item41['执行依据文号'] = lsscr.xpath('.//td[6]/text()')
        #         item['历史失信人信息'].append(item41)
        # else:
        #     item['历史失信人信息'] = '暂无历史失信人信息'

        # #司法协助
        # sifaxiezhu = response.xpath('//div[@class="block-data"]/div[@id="_container_judicialAid"]/table/tbody/tr')
        # if sifaxiezhu:
        #     item['司法协助'] = []
        #     for sfxz in sifaxiezhu:
        #         item42 = {}
        #         item42['序号'] = sfxz.xpath('.//td[1]/text()').extract_first()
        #         item42['被执行人'] = sfxz.xpath('.//td[2]/text()').extract_first()
        #         item42['股权数额'] = sfxz.xpath('.//td[3]/text()').extract_first()
        #         item42['执行法院'] = sfxz.xpath('.//td[4]/text()').extract_first()
        #         item42['执行通知文号'] = sfxz.xpath('.//td[5]/text()').extract_first()
        #         item42['类型|状态'] = sfxz.xpath('.//td[6]/text()').extract_first()
        #         item['司法协助'].append(item42)
        # else:
        #     item['司法协助'] = '暂无司法协助信息'

        # #司法拍卖
        # sifapaimai = response.xpath('//div[@class="block-data"]/div[@id="_container_judicialSale"]/table/tbody/tr')
        # if sifapaimai:
        #     item['司法拍卖'] = []
        #     for sfpm in sifapaimai:
        #         item43 = {}
        #         item43['序号'] = sfpm.xpath('.//td[1]/text()').extract_first()
        #         item43['拍卖公告'] = sfpm.xpath('.//td[2]/a/text()').extract_first()
        #         item43['拍卖公告url'] = sfpm.xpath('.//td[2]/a/@href').extract_first()
        #         item43['公告时间'] = sfpm.xpath('.//td[3]/text()').extract_first()
        #         item43['执行法院'] = sfpm.xpath('.//td[4]/text()').extract_first()
        #         paimaibiaodi = sfpm.xpath('.//td[5]')
        #         item43['拍卖标的'] = paimaibiaodi.xpath('string(.)').extract_first()
        #         item['司法拍卖'].append(item43)
        # else:
        #     item['司法拍卖'] = '暂无司法拍卖信息'

        # #历史动产抵押
        # lishidongchan = response.xpath('//div[@class="block-data"]/div[@id="_container_pastMortgageCount"]/table/tbody/tr')
        # if lishidongchan:
        #     item['历史动产抵押'] = []
        #     for lsdc in lishidongchan:
        #         item44 = {}
        #         item44['序号'] = sfpm.xpath('.//td[1]/text()').extract_first()
        #         item44['登记日期'] = sfpm.xpath('.//td[2]/text()').extract_first()
        #         item44['登记号'] = sfpm.xpath('.//td[3]/text()').extract_first()
        #         item44['被担保债权类型'] = sfpm.xpath('.//td[4]/text()').extract_first()
        #         item44['被担保债权数额'] = sfpm.xpath('.//td[5]/text()').extract_first()
        #         item44['登记机关'] = sfpm.xpath('.//td[6]/text()').extract_first()
        #         item44['状态'] = sfpm.xpath('.//td[7]/text()').extract_first()
        #         item['历史动产抵押'].append(item44)
        # else:
        #     item['历史动产抵押'] = '暂无历史动产抵押信息'

        # #动产抵押
        # dongchan = response.xpath('//div[@class="block-data"]/div[@id="_container_mortgage"]/table/tbody/tr')
        # if dongchan:
        #     item['动产抵押'] = []
        #     for dc in dongchan:
        #         item45 = {}
        #         item45['序号'] = sfpm.xpath('.//td[1]/text()').extract_first()
        #         item45['登记日期'] = sfpm.xpath('.//td[2]/text()').extract_first()
        #         item45['登记号'] = sfpm.xpath('.//td[3]/text()').extract_first()
        #         item45['被担保债权类型'] = sfpm.xpath('.//td[4]/text()').extract_first()
        #         item45['被担保债权数额'] = sfpm.xpath('.//td[5]/text()').extract_first()
        #         item45['登记机关'] = sfpm.xpath('.//td[6]/text()').extract_first()
        #         item45['状态'] = sfpm.xpath('.//td[7]/text()').extract_first()
        #         item['动产抵押'].append(item45)
        # else:
        #     item['动产抵押'] = '暂无动产抵押信息'

        # #失信人信息
        # shixinren = response.xpath('//div[@class="block-data"]/div[@id="_container_dishonest"]/table/tbody/tr')
        # if shixinren:
        #     item['失信人信息'] = []
        #     for sxr in shixinren:
        #         item46 = {}
        #         item46['序号'] = scr.xpath('.//td[1]/text()').extract_first()
        #         item46['立案日期'] = scr.xpath('.//td[2]/span/text()').extract_first()
        #         item46['案号'] = scr.xpath('.//td[3]/text()').extract_first()
        #         item46['执行法院'] = scr.xpath('.//td[4]/text()').extract_first()
        #         item46['执行法院'] = scr.xpath('.//td[4]/text()').extract_first()
        #         item46['履行状态'] = scr.xpath('.//td[5]/text()').extract_first()
        #         item46['执行依据文号'] = scr.xpath('.//td[6]/text()').extract_first()
        #         item['失信人信息'].append(item46)
        # else:
        #     item['失信人信息'] = '暂无失信人信息'

        # ##欠税公告
        # qianshuigonggao = response.xpath('//div[@class="block-data"]/div[@id="_container_zhixing"]//table/tbody/tr')
        # if qianshuigonggao:
        #     item['欠税公告'] = []
        #     for qsgg in qianshuigonggao:
        #         item47 = {}
        #         item47['序号'] = qsgg.xpath('.//td[1]/text()').extract_first()
        #         item47['发布日期'] = qsgg.xpath('.//td[2]/text()').extract_first()
        #         item47['纳税人识别号'] = qsgg.xpath('.//td[3]/text()').extract_first()
        #         item47['欠税税种'] = qsgg.xpath('.//td[4]/text()').extract_first()
        #         item47['当前发生的欠税额'] = qsgg.xpath('.//td[5]/text()').extract_first()
        #         item47['欠税余额'] = qsgg.xpath('.//td[6]/text()').extract_first()
        #         item47['税务机关'] = qsgg.xpath('.//td[5]/text()').extract_first()
        #         item['欠税公告'].append(item47)
        # else:
        #     item['欠税公告'] = '暂无欠税公告信息'

        # #严重违法
        # yanzhongweifa = response.xpath('//div[@class="block-data"]/div[@id="_container_illegal"]/table/tbody/tr')
        # if yanzhongweifa:
        #     item['严重违法'] = []
        #     for yzwf in yanzhongweifa:
        #         item47 = {}
        #         item47['序号'] = scr.xpath('.//td[1]/text()').extract_first()
        #         item47['列入日期'] = scr.xpath('.//td[2]/text()').extract_first()
        #         item47['列入原因'] = scr.xpath('.//td[3]/text()').extract_first()
        #         item47['决定机关'] = scr.xpath('.//td[4]/text()').extract_first()
        #         item['严重违法'].append(item47)
        # else:
        #     item['严重违法'] = '暂无严重违法信息'

        # yield item
