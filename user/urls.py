from django.urls import path
from . import views

urlpatterns = [
    path('saveCredentails', views.saveCredentails, name='saveCredentails'),
    path('savePassword', views.savePassword, name='savePassword'),
    path('', views.account, name='account'),
]
