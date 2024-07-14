from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.


from .tasks import get_nba_news


def trigger_crawler(request):
    get_nba_news.delay()
    return JsonResponse({'status': 'Crawler triggered!'})