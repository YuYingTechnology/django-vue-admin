from django.shortcuts import render
from rest_framework import viewsets
from oAuth.models import NewUser
from oAuth.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from oAuth.serializers import (
    WechatTokenObtainSerializer,
    DingTalkTokenObtainSerializer,
    FeiShuTokenObtainSerializer,
)
from django.db.models import ManyToOneRel


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user_info = NewUser.objects.filter(id=request.user.id).values()[0]
        role = request.user.roles
        if role == 0:
            user_info['roles'] = ['admin']
        else:
            user_info['roles'] = ['user']
        del user_info['password']
        user_info['name'] = user_info['first_name'] + user_info['last_name']

        return Response(user_info)


class WechatTokenObtainPairView(TokenObtainPairView):

    serializer_class = WechatTokenObtainSerializer

class DingTalkTokenObtainPairView(TokenObtainPairView):

    serializer_class = DingTalkTokenObtainSerializer

class FeiShuTokenObtainPairView(TokenObtainPairView):

    serializer_class = FeiShuTokenObtainSerializer
