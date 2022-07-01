from dataclasses import fields
from django.contrib.auth.models import User
from rest_framework import serializers

# 于文章列表中引用的嵌套序列化器
class UserDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined',
        ]