from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"
    
class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "agent"
    
class IsSurveyor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "surveyor"
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "customer"
    
class IsAgentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["agent","admin"]