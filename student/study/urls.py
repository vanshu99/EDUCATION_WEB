from django.urls import path
from . import views
urlpatterns = [
            path("home",views.home),
            path("about",views.about),
            path("contact",views.contact),
            path("login",views.login),
            path('verify',views.verify),
            path("saveContact",views.saveContact),
            path("register",views.register),
            path("loginuser",views.loginuser),
            path("logout",views.logout)  

            ]