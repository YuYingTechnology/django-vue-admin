import requests, json
from system.models import FeiShuManager

class FeiShu(object):

    def __init__(self):
        self.feishu_manager_info = FeiShuManager.objects.first()
        self.app_id = self.feishu_manager_info.app_id
        self.app_secret = self.feishu_manager_info.app_secret
        self.session = requests.Session()
        self.base_url = 'https://open.feishu.cn'
        self.get_access_token()

    def get_access_token(self):
        feishu_manager_info = FeiShuManager.objects.first()
        url = self.base_url + '/open-apis/auth/v3/tenant_access_token/internal'
        data = {
            'app_id': feishu_manager_info.app_id,
            'app_secret': feishu_manager_info.app_secret,
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = self.session.post(url, data=json.dumps(data), headers=headers)
        print(response)
        if 'tenant_access_token' in response.json():
            self.accessToken = response.json()['tenant_access_token']
        else:
            self.accessToken = None

    def get_user_info(self, code):
        url = self.base_url + '/open-apis/authen/v1/access_token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
        }
        headers = {
            'Authorization': 'Bearer ' + self.accessToken,
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = self.session.post(url, data=json.dumps(data), headers=headers)
        data = response.json()['data']
        if response.status_code == 200:
            if response.json()['code'] == 0:
                print(response.json())

                data = {
                    'name': data['name'],
                    'en_name': data['en_name'],
                    'union_id': data['union_id'],
                    'open_id': data['open_id'],
                    'avatar_big': data['avatar_big']
                }
                return data
        else:
            return None
