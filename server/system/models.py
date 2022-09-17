from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(verbose_name='中文名称', max_length=100, null=True, blank=True)
    en_name = models.CharField(verbose_name='英文名称', max_length=100, null=True, blank=True)
    router = models.CharField(verbose_name='英文名称', max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id) + '---' + self.name + '---' + self.en_name + '---' + self.router

    class Meta:
        verbose_name_plural = "菜单"


class WechatManager(models.Model):
    appid = models.CharField(verbose_name='企业微信id', max_length=99, unique=True)
    agentid = models.CharField(verbose_name='企业微信应用id', max_length=99, unique=True)
    corpsecret = models.CharField(verbose_name='企业微信应用secret', max_length=99, unique=True)

    class Meta:
        verbose_name_plural = "微信管理信息（企业微信登录必填）"


class DingTalkManager(models.Model):
    client_id = models.CharField(verbose_name='钉钉应用id', max_length=99, unique=True)
    clientSecret = models.CharField(verbose_name='钉钉应用secret', max_length=99, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.client_id + '---' + self.clientSecret

    class Meta:
        verbose_name_plural = "钉钉管理信息（钉钉登录必填）"


class FeiShuManager(models.Model):
    app_id = models.CharField(verbose_name='飞书应用id', max_length=99, unique=True)
    app_secret = models.CharField(verbose_name='飞书应用secret', max_length=99, unique=True)

    def __str__(self):
        return str(self.id) + '---' + self.app_id + '---' + self.app_secret

    class Meta:
        verbose_name_plural = "飞书管理信息（飞书登录必填）"