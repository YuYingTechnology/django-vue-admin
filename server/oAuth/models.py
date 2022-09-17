from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class NewUser(AbstractUser):

    role_type = [
        [0, 'admin'],
        [1, 'user'],
    ]

    roles = models.IntegerField(verbose_name='角色', choices=role_type, default=1)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, auto_now=True)
    wechat = models.OneToOneField('Wechat', null=True, blank=True, verbose_name='微信', on_delete=models.SET_NULL)
    dingtalk = models.OneToOneField('DingTalk', null=True, blank=True, verbose_name='钉钉', on_delete=models.SET_NULL)
    feishu = models.OneToOneField('FeiShu', null=True, blank=True, verbose_name='飞书', on_delete=models.SET_NULL)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        pass

class Wechat(models.Model):
    userid = models.CharField(verbose_name='企业微信id', max_length=99, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.userid

    class Meta:
        verbose_name_plural = "用户的微信信息"


class WechatManager(models.Model):
    appid = models.CharField(verbose_name='企业微信id', max_length=99, unique=True)
    agentid = models.CharField(verbose_name='企业微信应用id', max_length=99, unique=True)
    corpsecret = models.CharField(verbose_name='企业微信应用secret', max_length=99, unique=True)

    class Meta:
        verbose_name_plural = "微信管理信息（企业微信登录必填）"


class DingTalk(models.Model):
    nick = models.CharField(verbose_name='钉钉昵称', max_length=200, unique=True)
    unionId = models.CharField(verbose_name='钉钉unionId', max_length=200, unique=True)
    openId = models.CharField(verbose_name='钉钉openId', max_length=200, unique=True)
    avatarUrl = models.CharField(verbose_name='钉钉头像', max_length=200, unique=True)
    mobile = models.CharField(verbose_name='钉钉手机号', max_length=200, unique=True)
    stateCode = models.CharField(verbose_name='钉钉手机号国家代码', max_length=200, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.nick + '---' + self.openId + '---' + self.mobile

    class Meta:
        verbose_name_plural = "用户的钉钉信息"

class DingTalkManager(models.Model):
    client_id = models.CharField(verbose_name='钉钉应用id', max_length=99, unique=True)
    clientSecret = models.CharField(verbose_name='钉钉应用secret', max_length=99, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.client_id + '---' + self.clientSecret

    class Meta:
        verbose_name_plural = "钉钉管理信息（钉钉登录必填）"

class FeiShu(models.Model):
    name = models.CharField(verbose_name='飞书昵称', max_length=200, unique=True)
    en_name = models.CharField(verbose_name='飞书英文昵称', max_length=200, unique=True)
    union_id = models.CharField(verbose_name='飞书union_id', max_length=200, unique=True)
    open_id = models.CharField(verbose_name='飞书open_id', max_length=200, unique=True)
    avatar_big = models.CharField(verbose_name='飞书头像', max_length=200, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.name + '---' + self.en_name + '---' + self.open_id

    class Meta:
        verbose_name_plural = "用户的飞书信息"

class FeiShuManager(models.Model):
    app_id = models.CharField(verbose_name='飞书应用id', max_length=99, unique=True)
    app_secret = models.CharField(verbose_name='飞书应用secret', max_length=99, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.app_id + '---' + self.app_secret

    class Meta:
        verbose_name_plural = "飞书管理信息（飞书登录必填）"