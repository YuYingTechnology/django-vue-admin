import requests
from system.models import WechatManager

class Wechat(object):

    def __init__(self):
        self.wechat_manager_info = WechatManager.objects.first()
        self.corpid = self.wechat_manager_info.appid
        self.corpsecret = self.wechat_manager_info.corpsecret
        self.session = requests.Session()
        self.get_access_token()

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (self.corpid, self.corpsecret)
        response = self.session.get(url=url)
        print(response)
        self.token = response.json()['access_token']

    def get_userid(self, code):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo?access_token=%s&code=%s' % (self.token, code)
        response = self.session.get(url=url)
        print(response)
        if 'userid' in response.json():
            self.userid = response.json()['userid']
            return self.userid
        else:
            return None