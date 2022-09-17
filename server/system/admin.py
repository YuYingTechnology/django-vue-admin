from django.contrib import admin
from system.models import (
    Menu,
    WechatManager,
    DingTalkManager,
    FeiShuManager
)

# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'en_name', 'router')
    list_display_links = ('id', 'name', 'en_name', 'router')

admin.site.register(Menu, MenuAdmin)


class WechatManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'appid', 'agentid', 'corpsecret')
    list_display_links = ('id', 'appid', 'agentid', 'corpsecret')

admin.site.register(WechatManager, WechatManagerAdmin)


class DingTalkManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'clientSecret')
    list_display_links = ('id', 'client_id', 'clientSecret')

admin.site.register(DingTalkManager, DingTalkManagerAdmin)


class FeiShuManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_id', 'app_secret')
    list_display_links = ('id', 'app_id', 'app_secret')

admin.site.register(FeiShuManager, FeiShuManagerAdmin)