from oAuth.models import NewUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from oAuth.wechat import Wechat
from oAuth.ding_talk import DingTalk
from oAuth.fei_shu import FeiShu
from oAuth.models import NewUser
from oAuth.models import Wechat as WechatModel
from oAuth.models import DingTalk as DingTalkModel
from oAuth.models import FeiShu as FeiShuModel
from django.db.models import ManyToOneRel

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    column_list = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    # 动态生成el-table column_list
    def get_column_list(self, obj):

        serializer_fields_list = self.Meta.fields
        fields_list = NewUser._meta.get_fields()
        fields_name_dict = {field.name: field.verbose_name for field in fields_list if not isinstance(field, ManyToOneRel)}
        column_list = []
        for serializer_field in serializer_fields_list:
            if serializer_field in fields_name_dict and serializer_field != 'column_list':
                column_list.append(
                    {
                        'prop': serializer_field,
                        'label': fields_name_dict[serializer_field]
                    }
                )
            elif serializer_field != 'column_list':
                column_list.append(
                    {
                        'prop': serializer_field,
                        'label': serializer_field
                    }
                )
        return column_list

    class Meta:
        model = NewUser
        fields = ['id', 'url', 'username', 'name', 'email', 'is_staff', 'column_list']


class WechatTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["code"] = serializers.CharField()
        self.fields["state"] = serializers.CharField()
        self.fields["appid"] = serializers.CharField()

    def validate(self, attrs):
        state = attrs['state']
        if state == "Wechat":
            wechat = Wechat()
            userid = wechat.get_userid(code=attrs["code"])
            if userid:
                data = {}
                attrs['userid'] = userid
                user = NewUser.objects.filter(wechat__userid=userid)
                if user.exists():
                    self.user = user[0]
                else:
                    wechat_user = WechatModel.objects.filter(userid=userid)
                    if wechat_user.exists():
                        user = NewUser.objects.create(username=userid, wechat=wechat_user[0])
                        user.save()
                    else:
                        wechat_user = WechatModel.objects.create(userid=userid)
                        wechat_user.save()
                        user = NewUser.objects.create(username=userid, wechat=wechat_user)
                        user.save()
                    self.user = user

                refresh = self.get_token(self.user)

                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)

                if api_settings.UPDATE_LAST_LOGIN:
                    update_last_login(None, self.user)
                print(data)
                return data
            else:
                return False

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

class DingTalkTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["state"] = serializers.CharField()
        self.fields["authCode"] = serializers.CharField()
    def validate(self, attrs):
        state = attrs['state']
        if state == 'DingTalk':
            dingtalk = DingTalk(authCode=attrs["authCode"])
            dingtalk_user_info = dingtalk.get_user_info()
            if dingtalk_user_info:
                data = {}
                openId = dingtalk_user_info['openId']
                user = NewUser.objects.filter(dingtalk__openId=openId)
                if user.exists():
                    self.user = user[0]
                else:
                    dingtalk_user = DingTalkModel.objects.filter(openId=openId)
                    if dingtalk_user.exists():
                        user = NewUser.objects.create(username=openId, dingtalk=dingtalk_user[0])
                        user.save()
                    else:
                        dingtalk_user = DingTalkModel.objects.create(**dingtalk_user_info)
                        dingtalk_user.save()
                        user = NewUser.objects.create(username=openId, dingtalk=dingtalk_user)
                        user.save()
                    self.user = user

                refresh = self.get_token(self.user)

                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)

                if api_settings.UPDATE_LAST_LOGIN:
                    update_last_login(None, self.user)
                print(data)
                return data
            else:
                return False
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

class FeiShuTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["state"] = serializers.CharField()
        self.fields["code"] = serializers.CharField()
    def validate(self, attrs):
        state = attrs['state']
        if state == 'FeiShu':
            feishu = FeiShu()
            feishu_user_info = feishu.get_user_info(code=attrs['code'])
            if feishu_user_info:
                data = {}
                open_id = feishu_user_info['open_id']
                user = NewUser.objects.filter(feishu__open_id=open_id)
                if user.exists():
                    self.user = user[0]
                else:
                    feishu_user = FeiShuModel.objects.filter(open_id=open_id)
                    if feishu_user.exists():
                        user = NewUser.objects.create(username=open_id, feishu=feishu_user[0])
                        user.save()
                    else:
                        feishu_user = FeiShuModel.objects.create(**feishu_user_info)
                        feishu_user.save()
                        user = NewUser.objects.create(username=open_id, feishu=feishu_user)
                        user.save()
                    self.user = user

                refresh = self.get_token(self.user)

                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)

                if api_settings.UPDATE_LAST_LOGIN:
                    update_last_login(None, self.user)
                print(data)
                return data
            else:
                return False
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)