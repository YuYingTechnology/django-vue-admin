from django.shortcuts import render
from rest_framework import viewsets
from system.models import (
    WechatManager,
    DingTalkManager,
    FeiShuManager
)
from urllib.parse import quote
from rest_framework.response import Response

# Create your views here.

class QRcodeViewSet(viewsets.ViewSet):
    queryset = WechatManager.objects.all()
    http_method_names = ['get']
    authentication_classes = []
    permission_classes = []

    def list(self, request, *args, **kwargs):
        wechat_manager_info = WechatManager.objects.all()
        dingtalk_manager_info = DingTalkManager.objects.all()
        feishu_manager_info = FeiShuManager.objects.all()
        data = {
            'wechat_qr_code_url': '',
            'dingtalk_qr_code_url': '',
            'feishu_qr_code_url': ''
        }
        try:
            wechat_redirect_uri = quote(request.META['HTTP_DOMAIN'] + '/wechat/login', safe='')
            dingtalk_redirect_uri = quote(request.META['HTTP_DOMAIN'] + '/dingtalk/login', safe='')
            feishu_redirect_uri = quote(request.META['HTTP_DOMAIN'] + '/feishu/login', safe='')

            if wechat_manager_info.exists():
                wechat_manager_info = self.queryset.values()[0]
                wechat_qr_code_url = 'https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=%s&agentid=%s&redirect_uri=%s&state=Wechat#wechat_redirect' %(wechat_manager_info['appid'], wechat_manager_info['agentid'], wechat_redirect_uri)
                data['wechat_qr_code_url'] = wechat_qr_code_url

            if dingtalk_manager_info.exists():
                dingtalk_manager_info = dingtalk_manager_info[0]
                dingtalk_qr_code_url = 'https://login.dingtalk.com/oauth2/challenge.htm?redirect_uri=%s&response_type=code&client_id=%s&scope=openid&state=DingTalk&prompt=consent' % (dingtalk_redirect_uri, dingtalk_manager_info.client_id)
                data['dingtalk_qr_code_url'] = dingtalk_qr_code_url

            if feishu_manager_info.exists():
                feishu_manager_info = feishu_manager_info[0]
                feishu_qr_code_url = 'https://open.feishu.cn/open-apis/authen/v1/index?app_id=%s&redirect_uri=%s&state=FeiShu' % (feishu_manager_info.app_id, feishu_redirect_uri)
                data['feishu_qr_code_url'] = feishu_qr_code_url

            return Response(data, status=200)
        except Exception as e:
            return Response(data, status=200)