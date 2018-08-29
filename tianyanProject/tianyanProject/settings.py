# -*- coding: utf-8 -*-

# Scrapy settings for tianyanProject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tianyanProject'

SPIDER_MODULES = ['tianyanProject.spiders']
NEWSPIDER_MODULE = 'tianyanProject.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyanProject (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tianyanProject.middlewares.TianyanprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'tianyanProject.middlewares.TianyanprojectDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'tianyanProject.pipelines.TianyanprojectPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HTTPERROR_ALLOWED_CODES = [301,302]

COOKIES = {'TYCID': '76822b70919f11e88d9b276aad8359cc', 'undefined': '76822b70919f11e88d9b276aad8359cc', 'ssuid': '9038734756', '_ga': 'GA1.2.1640785305.1532919826', 'jsid': 'SEM-BAIDU-CG-SY-002243', 'tyc-user-info': '%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc0NjU3MjE3MCIsImlhdCI6MTUzNTA4MTkxMCwiZXhwIjoxNTUwNjMzOTEwfQ.VLqhgWh0lJS8KrbMoV1YmTPHxreIdD1UJ77IHR_bpLbxHTEtpoTTgHcWFgr5EJx_H7IRsTFd8g7zejdohfqykg%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217746572170%2522%257D', 'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc0NjU3MjE3MCIsImlhdCI6MTUzNTA4MTkxMCwiZXhwIjoxNTUwNjMzOTEwfQ.VLqhgWh0lJS8KrbMoV1YmTPHxreIdD1UJ77IHR_bpLbxHTEtpoTTgHcWFgr5EJx_H7IRsTFd8g7zejdohfqykg', '_gid': 'GA1.2.471341609.1535333091', 'RTYCID': '2f53bcb942fe47cc96619935afa396e9', 'CT_TYCID': 'acb63adcb1304d6daf72f0af7ffdfa95', 'aliyungf_tc': 'AQAAAOv0UQR7og4Acop3AbOEJneECfxP', 'csrfToken': '3sI2WJWQVVPfHy-oeF3fMKMk', 'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1533902784,1535075472,1535333091,1535421893', 'bannerFlag': 'true', 'cloud_token': 'd49d5ef1fdfe47298f1155320f1cd389', 'cloud_utm': '0b1c95ca48d445238c1b04399bf1b9f0', 'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1535422086'}

DEFAULT_REQUEST_HEADERS = {
# 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding':'gzip, deflate, br',
# 'Accept-Language':'en-GB,en;q=0.5',
# 'Cache-Control': 'max-age=0',
# 'Connection':'keep-alive',
# 'Host':'www.tianyancha.com',
# 'Upgrade-Insecure-Requests':'1',
# 'User-Agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'www.tianyancha.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

headers2 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/search?key=%E6%9D%BE%E9%BC%A0%E5%B1%B1%E7%A7%91%E6%8A%80',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Host': 'www.tianyancha.com',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# USER_AGENTS = [
#     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#     'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
# ]

# HTTP_PROXY=[
#     {'ip_port': '27.44.196.105:9999', 'user_pass': ''},
#     {'ip_port': '113.87.160.206:9000', 'user_pass': ''},
#     {'ip_port': '112.67.173.17:9797', 'user_pass': ''},
# ]

# proxys = [
#     {"port": "8888", "ip": "60.168.11.238"}, {"port": "9797", "ip": "112.67.168.236"},
#     {"port": "63909", "ip": "183.163.37.184"}, {"port": "80", "ip": "223.223.187.195"},
#     {"port": "9797", "ip": "112.67.168.236"}, {"port": "63909", "ip": "183.163.37.184"},
#     {"port": "9000", "ip": "221.217.54.195"}, {"port": "9797", "ip": "171.37.140.218"},
#     {"port": "3128", "ip": "58.209.240.25"}, {"port": "53281", "ip": "114.101.18.168"},
#     {"port": "8888", "ip": "112.95.205.126"}, {"port": "9797", "ip": "14.115.107.3"},]

# RETRY_ENABLED = True
# RETRY_TIMES = 20  
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 403]
# RETRY_PRIORITY_ADJUST = -1

