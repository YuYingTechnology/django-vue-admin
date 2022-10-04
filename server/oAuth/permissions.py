from rest_framework.permissions import (
    BasePermission,
    DjangoModelPermissions
)

class IsOwer(BasePermission):
    """
    判断当前用户是否在操作自己的数据，比如只允许用户修改自己的资料。
    不允许用户修改“超级用户状态”、“有效状态”、“用户组（角色）”
    请注意：
        1. 超级管理员（is_superuser = True）用户，不受该策略控制
        2. 用户、或者用户所在分组，拥有 “oAuth | 用户 | Can change user” 权限时，不受该策略控制
    """

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if 'is_superuser' in request.data or 'is_active' in request.data \
                or 'groups' in request.data or 'wechat' in request.data:
            return False

        # if ('is_superuser' in request.data and request.data['is_superuser'] != obj.is_superuser) \
        #         or ('is_active' in request.data and request.data['is_active'] != obj.is_active) \
        #         or ('groups' in request.data and request.data['groups'] != groups_id_list) \
        #         or ('wechat' in request.data and request.data['wechat'] != obj.wechat):
        #     return False
        return request.user == obj

class NewDjangoModelPermissions(DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }