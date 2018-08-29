class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        # items = self.cookie.split(';')
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":

    cookie = "TYCID=76822b70919f11e88d9b276aad8359cc; undefined=76822b70919f11e88d9b276aad8359cc; ssuid=9038734756; _ga=GA1.2.1640785305.1532919826; jsid=SEM-BAIDU-CG-SY-002243; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc0NjU3MjE3MCIsImlhdCI6MTUzNTA4MTkxMCwiZXhwIjoxNTUwNjMzOTEwfQ.VLqhgWh0lJS8KrbMoV1YmTPHxreIdD1UJ77IHR_bpLbxHTEtpoTTgHcWFgr5EJx_H7IRsTFd8g7zejdohfqykg%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217746572170%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc0NjU3MjE3MCIsImlhdCI6MTUzNTA4MTkxMCwiZXhwIjoxNTUwNjMzOTEwfQ.VLqhgWh0lJS8KrbMoV1YmTPHxreIdD1UJ77IHR_bpLbxHTEtpoTTgHcWFgr5EJx_H7IRsTFd8g7zejdohfqykg; _gid=GA1.2.471341609.1535333091; RTYCID=2f53bcb942fe47cc96619935afa396e9; CT_TYCID=acb63adcb1304d6daf72f0af7ffdfa95; aliyungf_tc=AQAAAOv0UQR7og4Acop3AbOEJneECfxP; csrfToken=3sI2WJWQVVPfHy-oeF3fMKMk; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1533902784,1535075472,1535333091,1535421893; bannerFlag=true; cloud_token=d49d5ef1fdfe47298f1155320f1cd389; cloud_utm=0b1c95ca48d445238c1b04399bf1b9f0; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1535422086"
    trans = transCookie(cookie)
    print(trans.stringToDict())