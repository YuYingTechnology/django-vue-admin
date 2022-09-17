import requests, json
from system.models import DingTalkManager

class DingTalk(object):

    def __init__(self, authCode):
        self.base_url = 'https://api.dingtalk.com'
        self.session = requests.Session()
        self.authCode = authCode
        self.get_access_token()
        self.dingtao_manager_info = DingTalkManager.objects.first()

    def get_access_token(self):
        dingtao_manager_info = DingTalkManager.objects.first()
        url = self.base_url + '/v1.0/oauth2/userAccessToken'
        data = {
            "clientId": dingtao_manager_info.client_id,
            "clientSecret": dingtao_manager_info.clientSecret,
            "code": self.authCode,
            "grantType": "authorization_code"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.session.post(url, data=json.dumps(data), headers=headers)
        print(response)
        if 'accessToken' in response.json():
            self.accessToken = response.json()['accessToken']
        else:
            self.accessToken = None

    def get_user_info(self):
        url = self.base_url + '/v1.0/contact/users/me'
        headers = {
            "x-acs-dingtalk-access-token": self.accessToken,
            "Content-Type": "application/json"
        }
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:

            print(response.json())
            return response.json()
        else:
            return None
