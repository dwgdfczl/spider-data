

import random
import base64
# import urllib2
import json
from ..settings import HTTP_PROXY,proxys


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # result = urllib2.Request("http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20187275530oW499V/c70f833b7db611e7bcaf7cd30abda612?returnType=2")
        # es_data = urllib2.urlopen(result)
        # res = es_data.read()
        # jsonres = json.loads(res)
        # ip_address = jsonres['RESULT']['wanIp']+':'+jsonres['RESULT']['proxyport']
        # pox = {'ip_port': ip_address, 'user_pass': ''}

        proxy = random.choice(proxys)
        print("**************ProxyMiddleware no pass************" + proxy['ip'])
        request.meta['proxy'] = "http://" + proxy['ip'] + ":" +  proxy['port']
        # if proxy['user_pass'] is not None:
        #     request.meta['proxy'] = "http://%s" % proxy['ip_port']
        #     encoded_user_pass = base64.encodestring(proxy['user_pass'])
        #     request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        #     print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        # else:
        #     print "**************ProxyMiddleware no pass************" + proxy['ip_port']
        #     request.meta['proxy'] = "http://%s" % proxy['ip_port']