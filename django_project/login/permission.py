from rest_framework.permissions import BasePermission

class IsOperator(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role=='operator')
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role=='manager')
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'manager' and request.user.is_manager_approved:
            return True
        else:
            return False

class IsOperatorOrManager(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role in ['operator', 'manager'])
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'manager':
            return True
        return obj.operator == request.user
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
