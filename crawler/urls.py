from django.urls import path
from .views import trigger_crawler

urlpatterns = [
    path('trigger-crawler/', trigger_crawler, name='trigger-crawler'),
]