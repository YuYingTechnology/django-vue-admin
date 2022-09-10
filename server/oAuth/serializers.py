from oAuth.models import NewUser
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
from django.contrib.auth.models import update_last_login
from oAuth.wechat import Wechat
from oAuth.models import NewUser
from oAuth.models import Wechat as WechatModel

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = NewUser
        fields = ['url', 'username', 'email', 'is_staff', 'name']

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