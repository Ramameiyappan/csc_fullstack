from django.urls import path, include
from .views import Register, Login, Refresh, Logout, GoogleJWTLogin, RequestManager, ApproveManager, RejectManager, PendingManagerRequests

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path("google/jwt/", GoogleJWTLogin.as_view(), name='google-jwt'),
    path('refresh/', Refresh.as_view(), name='refresh'),
    path('request-manager/', RequestManager.as_view(), name='request_manager'),
    path('manager-requests/', PendingManagerRequests.as_view(), name='manager_request'),
    path('manager-approve/<int:user_id>/', ApproveManager.as_view(), name='manager_approve'),
    path('manager-reject/<int:user_id>/', RejectManager.as_view(), name='manager_reject'),
    path('logout/', Logout.as_view(), name='logout')
]