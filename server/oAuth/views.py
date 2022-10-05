from django.shortcuts import render
from rest_framework import (
    viewsets,
    filters
)
from oAuth.models import (
    NewUser,
    Wechat,
    FeiShu,
    DingTalk
)
from oAuth.serializers import (
    UserSerializer,
    WechatSerializer,
    FeiShuSerializer,
    DingTalkSerializer,
    UserUpdateSerializer,
    GroupsSerializer,
    PermissionSerializer
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from oAuth.serializers import (
    WechatTokenObtainSerializer,
    DingTalkTokenObtainSerializer,
    FeiShuTokenObtainSerializer,
)
from utils.column_list import get_column_list
from django.contrib.auth.models import (
    Group,
    Permission
)
from oAuth.permissions import (
    IsOwer,
    NewDjangoModelPermissions
)


class PermissionModelViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [NewDjangoModelPermissions]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name', 'content_type', 'codename']
    ordering_fields = '__all__'


class GroupModelViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [NewDjangoModelPermissions]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):

        # 获取column_list， 为前端table展示用
        serializer_fields_list = self.serializer_class.Meta.fields
        fields_list = NewUser._meta.get_fields()
        column_list = get_column_list(serializer_fields_list=serializer_fields_list, fields_list=fields_list)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['column_list'] = column_list
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsOwer|NewDjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'username', 'last_name', 'first_name', 'email', 'wechat__userid']

    def list(self, request, *args, **kwargs):
        # 获取column_list， 为前端table展示用
        serializer_fields_list = self.serializer_class.Meta.fields
        fields_list = NewUser._meta.get_fields()
        column_list = get_column_list(serializer_fields_list=serializer_fields_list, fields_list=fields_list)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['column_list'] = column_list
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class WechatModelViewSet(viewsets.ModelViewSet):
    queryset = Wechat.objects.all().order_by('id')
    serializer_class = WechatSerializer
    permission_classes = [NewDjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'userid']

    def list(self, request, *args, **kwargs):

        # 获取column_list， 为前端table展示用
        serializer_fields_list = self.serializer_class.Meta.fields
        fields_list = Wechat._meta.get_fields()
        column_list = get_column_list(serializer_fields_list=serializer_fields_list, fields_list=fields_list)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['column_list'] = column_list
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FeiShuModelViewSet(viewsets.ModelViewSet):
    queryset = FeiShu.objects.all().order_by('id')
    serializer_class = FeiShuSerializer
    permission_classes = [NewDjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'name', 'en_name', 'union_id', 'open_id']

    def list(self, request, *args, **kwargs):

        # 获取column_list， 为前端table展示用
        serializer_fields_list = self.serializer_class.Meta.fields
        fields_list = FeiShu._meta.get_fields()
        column_list = get_column_list(serializer_fields_list=serializer_fields_list, fields_list=fields_list)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['column_list'] = column_list
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DingTalkModelViewSet(viewsets.ModelViewSet):
    queryset = DingTalk.objects.all().order_by('id')
    serializer_class = DingTalkSerializer
    permission_classes = [NewDjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'nick', 'unionId', 'openId', 'mobile']

    def list(self, request, *args, **kwargs):

        # 获取column_list， 为前端table展示用
        serializer_fields_list = self.serializer_class.Meta.fields
        fields_list = DingTalk._meta.get_fields()
        column_list = get_column_list(serializer_fields_list=serializer_fields_list, fields_list=fields_list)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['column_list'] = column_list
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user_info = NewUser.objects.filter(id=request.user.id).values()[0]
        groups = NewUser.objects.filter(id=request.user.id).values_list('groups__name', flat=True)

        user_info['roles'] =groups
        del user_info['password']
        user_info['name'] = user_info['last_name'] + ' ' + user_info['first_name']

        return Response(user_info)


class WechatTokenObtainPairView(TokenObtainPairView):

    serializer_class = WechatTokenObtainSerializer


class DingTalkTokenObtainPairView(TokenObtainPairView):

    serializer_class = DingTalkTokenObtainSerializer


class FeiShuTokenObtainPairView(TokenObtainPairView):

    serializer_class = FeiShuTokenObtainSerializer
