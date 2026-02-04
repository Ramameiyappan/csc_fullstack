from django.urls import path
from .views import (Electricity, Recharge, Pan, Travel, 
                    Insurance, Online, Esevai, Topup, 
                    LedgerDashboard, UserDashboard)

urlpatterns = [
    path('electricity/', Electricity.as_view(), name='electricity'),
    path('recharge/', Recharge.as_view(), name='recharge'),
    path('pan/', Pan.as_view(), name='pan'),
    path('travel/', Travel.as_view(), name='travel'),
    path('insurance/', Insurance.as_view(), name='insurance'),
    path('online/', Online.as_view(), name='online'),
    path('esevai/', Esevai.as_view(), name='esevai'),
    path('topup/', Topup.as_view(), name='topup'),
    path('dashboard/', LedgerDashboard.as_view(), name='dashboard'),
    path('userdetail/', UserDashboard.as_view(), name='userdashboard')
]