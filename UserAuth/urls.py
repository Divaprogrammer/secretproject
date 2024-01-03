from django.urls import path
from .views import UserRegistration,UserLogin,UserLogout,UserForgot


urlpatterns = [
    path('signin/',UserRegistration.as_view(),name='Register'),
    path('signup/',UserLogin.as_view(),name='Login'),
    path('logout/',UserLogout.as_view(),name='Logout'),
    path('userforgot/',UserForgot.as_view(),name='UserForgot')
]