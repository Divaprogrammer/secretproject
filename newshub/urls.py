from django.urls import path
from .views import (
                    LandingPage,
                    CategoryPage,
                    SearchingPage,
                    AllNews,
                    GetNewsDetails)

urlpatterns = [
    path('',LandingPage.as_view(),name='LandingPage'),
    path('category/',CategoryPage.as_view(),name='CategoryPage'),
    path('search/',SearchingPage.as_view(),name='SearchingPage'),
    path('latest/',AllNews.as_view(),name='AllNews'),
    path('details/',GetNewsDetails.as_view(),name='GetNewsDetails'),
]