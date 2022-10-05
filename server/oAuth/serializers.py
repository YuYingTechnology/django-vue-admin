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
from datetime import timedelta
from django.contrib.auth.models import Group, Permission


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('__all__')

class WechatSerializer(serializers.ModelSerializer):
    bound = serializers.SerializerMethodField()

    def get_bound(self, obj):
        print(obj)
        try:
            obj.wechat_user
            return True
        except:
            return False

    class Meta:
        model = WechatModel
        fields = ('__all__')


class DingTalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = DingTalkModel
        fields = ('__all__')


class FeiShuSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeiShuModel
        fields = ('__all__')


class GroupsSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class UserSerializer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField()
    # wechat = serializers.SerializerMethodField()
    # dingtalk = serializers.SerializerMethodField()
    # feishu = serializers.SerializerMethodField()
    wechat = WechatSerializer()
    dingtalk = DingTalkSerializer()
    feishu = FeiShuSerializer()
    groups = GroupsSerializer(many=True)
    last_login = serializers.SerializerMethodField()
    user_permissions = PermissionSerializer(many=True)

    # def get_name(self, obj):
    #     return obj.last_name + ' ' + obj.first_name

    def get_last_login(self, obj):
        return (obj.last_login + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = NewUser
        fields = ['id', 'url', 'username', 'user_permissions', 'last_name', 'first_name', 'wechat', 'dingtalk', 'feishu', 'email', 'groups', 'is_active', 'is_superuser', 'last_login']

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('__all__')


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
                        user.groups.add(Group.objects.get(name='user'))
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
                        user.groups.add(Group.objects.get(name='user'))
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
                        user.groups.add(Group.objects.get(name='user'))
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