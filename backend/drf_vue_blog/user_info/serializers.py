from cgitb import lookup
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

# 用户注册
class UserRegisterSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username') # lookup_field指定了解析超链接关系的字段，将其配置为username后，用户详情接口的地址表示为用户名而不是id

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'password'
        ]
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) # 两个*表示收集关键字参数
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password) # 密码需要单独拿出来通过set_password()方法加密后存储，而不能以明文的形式保存
        return super().update(instance, validated_data)

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_name',
            'first_name',
            'email',
            'last_login',
            'date_joined'
        ]
        
