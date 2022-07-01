from email import message
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner to update'

    def safe_methods_or_owner(self, request, func):
        if request.method in SAFE_METHODS:
            return True

        return func()
    # 这个方法早于视图集中的perform_create方法，在这个方法中可以验证用户是否登录，否则若未登录就直接创建评论，会报错
    def has_permission(self, request, view):
        return self.safe_methods_or_owner(
            request,
            lambda: request.user.is_authenticated
        )
    # 验证用户是否为评论人
    def has_object_permission(self, request, view, obj):
        return self.safe_methods_or_owner(
            request,
            lambda: obj.author == request.user
        )


    # def has_permission(self, request, view):
    #     if request.method in SAFE_METHODS:
    #         return True
    #     return request.user.is_authenticated

    # def has_object_permission(self, request, view, obj):
    #     if request.method in SAFE_METHODS:
    #         return True
    #     return obj.author == request.user