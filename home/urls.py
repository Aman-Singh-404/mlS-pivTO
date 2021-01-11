from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.userlogin, name = "login"),
    path("createAccount/",views.createAccount, name = "createAccount"),
    path("signup/", views.signup, name = "signup"),
    path("logout/", views.userlogout, name = "logout"),
    path("passwordValidation/", views.passwordValidation, name = "passwordValidation"),
    path("", views.homepage, name = "homepage"),
]
