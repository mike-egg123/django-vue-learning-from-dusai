from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from article import serializers

from user_info.serializers import UserRegisterSerializer, UserDetailSerializer
from user_info.permissions import IsSelfOrReadOnly

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]
        
        return super().get_permissions()

    # 使用装饰器action来自定义动作，此动作可以获得用户的超详细信息
    @action(detail=True, methods=['get'])
    def info(self, request, username=None):
        queryset = User.objects.get(username=username)
        serializer = UserDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    # 此动作可以获得排序并分页好的用户信息
    @action(detail=False)
    def sorted(self, request):
        users = User.objects.all().order_by('-username')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

