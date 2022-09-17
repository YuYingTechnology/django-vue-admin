from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from oAuth.models import (
    NewUser,
    Wechat,
    DingTalk,
    FeiShu,
)

# Register your models here.


class NewUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'group', 'password')}),
        (_('Personal info'), {'fields': ('email', 'wechat', 'dingtalk', 'feishu', 'first_name', 'last_name' )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'roles')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )

    list_display = ('id', 'username', 'wechat', 'dingtalk', 'feishu', 'roles', 'email', 'is_active', 'last_login')
    list_display_links = ('id', 'username', 'wechat', 'dingtalk', 'feishu', 'roles', 'email', 'last_login')
    search_fields = ('username', 'email', 'wechat', 'dingtalk')


admin.site.register(NewUser, NewUserAdmin)


class WechatAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid')
    list_display_links = ('id', 'userid')

admin.site.register(Wechat, WechatAdmin)


class DingTalkAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick', 'unionId', 'openId', 'avatarUrl', 'mobile', 'stateCode')
    list_display_links = ('id', 'nick', 'unionId', 'openId', 'avatarUrl', 'mobile', 'stateCode')

admin.site.register(DingTalk, DingTalkAdmin)


class FeiShuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'en_name', 'union_id', 'open_id', 'avatar_big')
    list_display_links = ('id', 'name', 'en_name', 'union_id', 'open_id', 'avatar_big')

admin.site.register(FeiShu, FeiShuAdmin)
