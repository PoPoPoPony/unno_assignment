from django.urls import path
from .views import NewsListAPIView, NewsAPIView, get_image, get_thumbnail

urlpatterns = [
    path('newslist/', NewsListAPIView.as_view(), name='get_news_list'),
    path('news/<str:news_id>/', NewsAPIView.as_view(), name='get_news'),
    path('media/covers/<str:cover_id>/', get_image, name='get_image'),
    path('media/thumbnails/<str:cover_id>/', get_thumbnail, name='get_thumbnail'),
]