from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager
)
from django.utils.translation import gettext_lazy as _
from system.models import Menu

# Create your models here.


class NewUser(AbstractUser):

    last_login = models.DateTimeField(_('last login'), blank=True, null=True, auto_now=True)
    wechat = models.OneToOneField('Wechat', null=True, blank=True, verbose_name='企业微信', on_delete=models.SET_NULL, related_name='wechat_user')
    dingtalk = models.OneToOneField('DingTalk', null=True, blank=True, verbose_name='钉钉', on_delete=models.SET_NULL, related_name='wechat_dingtalk')
    feishu = models.OneToOneField('FeiShu', null=True, blank=True, verbose_name='飞书', on_delete=models.SET_NULL, related_name='wechat_feishu')
    menu = models.ManyToManyField(Menu, blank=True, verbose_name='菜单', related_name='menu')

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