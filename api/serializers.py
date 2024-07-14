from rest_framework import serializers
from crawler.models import News, Tags, Covers, Sources
from django.conf import settings
import os


class APIImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        url = f'http://localhost:{os.getenv("DJANGO_PORT")}/api{settings.MEDIA_URL}{value}'
        # url = f'{settings.MEDIA_URL}{value}'
        return url
    

class NewsPreviewSerializer(serializers.ModelSerializer):
    covers_thumbnail = APIImageField(source='covers.thumbnail')

    class Meta:
        model = News
        fields = ('news_id', 'title', 'pub_date', 'content', 'covers_thumbnail')


class SourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sources
        fields = ('name', 'author', 'category')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name',)

class CoversSerializer(serializers.ModelSerializer):
    caption = serializers.CharField()

    class Meta:
        model = Covers
        fields = ('caption',)


class NewsSerializer(serializers.ModelSerializer):
    covers_cover_image = APIImageField(source='covers.image')
    sources = SourcesSerializer()
    covers = CoversSerializer()
    tags = TagsSerializer(many=True)

    class Meta:
        model = News
        fields = ('news_id', 'title', 'pub_date', 'content', 'tags', 'covers', 'covers_cover_image', 'sources')
