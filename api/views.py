from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from django.http import JsonResponse, HttpResponse
from crawler.models import News, Covers, Tags, Sources
from .serializers import NewsPreviewSerializer, NewsSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

# Create your views here.
class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsPreviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        limit = int(self.request.query_params.get('limit', len(queryset)))
        offset = int(self.request.query_params.get('offset', 0))
        

        if offset+limit>len(queryset):
            queryset=[]
        else:
            queryset=queryset[offset:offset+limit]

        return queryset


class NewsAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        queryset = News.objects.filter(news_id=news_id)
        
        return queryset


def get_news(request):
    return JsonResponse({'status': 'get_news triggered!'})


def get_image(request, cover_id):
    try:
        cover = get_object_or_404(Covers, image=f"covers/{cover_id}")
        cover_image_path = os.path.join(settings.MEDIA_ROOT, cover.image.name)

        if os.path.exists(cover_image_path):
            with open(cover_image_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/png')
        else:
            return JsonResponse({'error': 'cover image not found'}, status=404)
    except FileNotFoundError:
        return JsonResponse({'error': 'Cover not found'}, status=404)

def get_thumbnail(request, cover_id):
    try:
        cover = get_object_or_404(Covers, thumbnail=f"thumbnails/{cover_id}")
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, cover.thumbnail.name)


        if os.path.exists(thumbnail_path):
            with open(thumbnail_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/png') 
        else:
            return JsonResponse({'error': 'Thumbnail not found'}, status=404)
    except FileNotFoundError:
        return JsonResponse({'error': 'Cover not found'}, status=404)