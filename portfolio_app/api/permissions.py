from rest_framework import permissions

class PortfolioUserOrAdminElseReadonly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_admin or (request.user == obj.owner) or obj.is_public:
                return True
            else:
                return False
            

class IsAdminOrAuthenticatedReadOnly(permissions.IsAuthenticated):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        if bool(request.user.is_superuser or request.user.is_staff):
            return True

        return False
    
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if bool(request.user.is_superuser or request.user.is_staff):
            return True
        
        return False
    
class PortfolioUserOrAdminCanEdit(permissions.IsAuthenticated):
    def has_object_permission(self,request,view,obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        elif obj.portfolio.owner == request.user:
            return True
        elif obj.portfolio.is_public and request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False