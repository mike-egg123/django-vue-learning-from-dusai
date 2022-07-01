from rest_framework import permissions

class isAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 只有管理员才可以进行所有操作（读写），而普通用户只能进行安全操作（读）
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser