from .views import NewsAPIView
from django.urls import path

urlpatterns = [
    # path('search/', search_news, name='search_news'),
    path('insert/', NewsAPIView.as_view(), name='news_api'),
]