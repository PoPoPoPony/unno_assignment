from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from bs4 import BeautifulSoup
from .models import News, Tags, Covers, Sources
from django.core.files.base import ContentFile
from typing import List
from datetime import datetime
import os
from django.db import transaction
from websocket.consumers import Consumer

class NBANews():
    def __init__(
            self,
            id_:str=None,
            title:str=None,
            pub_date:datetime=None,
            source_name:str=None,
            source_author:str=None,
            source_category:str=None,
            cover_image_url:str=None,
            cover_thumbnail_url:str=None,
            cover_caption:str=None,
            content:str=None,
            tags:str=None
        ) -> None:
        self.id=id_
        self.title=title
        self.pub_date=pub_date
        self.source_name=source_name
        self.source_author=source_author
        self.source_category=source_category
        self.cover_image_url=cover_image_url
        self.cover_thumbnail_url=cover_thumbnail_url
        self.cover_caption=cover_caption
        self.content=content
        self.tags=tags

    def tag_str_to_list(self) -> None:
        if isinstance(self.tags, str):
            self.tags = self.tags.split(",")



@shared_task(name='get_nba_news')
def get_nba_news():
    all_nba_news_dict=[]

    # [首頁]的新聞滑到最下面只會call 5次獲取新聞的api，因此這邊先做個5次
    for page_i in range(1, 6):
        # url = 'https://tw-nba.udn.com/nba/index'
        url=f'https://tw-nba.udn.com/api/more?channel_id=2000&type=index&page={page_i}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = soup.find_all('dt')
        links = []
        for news in news_list:
            link=news.find('a').get('href')
            links.append(link)

        for link in links:
            news_id=link.split("/")[-1]

            response = requests.get(link)
            soup=BeautifulSoup(response.text, 'html.parser')
            article=soup.find(id="story_body_content")

            # find title
            title=article.find('h1').text

            # find author and pub_date
            source_div=article.find(class_='shareBar__info--author')
            pub_date=source_div.find('span').text
            
            source=source_div.text
            source=source[len(pub_date):]
            # 有些左斜線是全形的
            source=source.replace('／', '/')
            source=source.split("/")

            if len(source)==2:
                source_name, source_category=(s.strip() for s in source)
                source_author=None
            elif len(source)==3:
                source_name, source_author, source_category=(s.strip() for s in source)

            cover=article.find('figure').find('img')
            cover_image_url=cover.get('src')
            cover_caption=cover.get('alt')
            cover_thumbnail_url=cover_image_url+'&w=220'
            date_format = "%Y-%m-%d %H:%M" 
            pub_date = datetime.strptime(pub_date, date_format)
            
            # find content
            contents=[]
            p_tags=article.find_all('p')
            for p_tag in p_tags:
                if p_tag.text is not None and len(p_tag.text.strip())>0:
                    if cover_caption not in p_tag.text:
                        contents.append(p_tag.text.strip())

            contents=''.join(contents)

            tags_div=soup.find(id='story_tags')
            tag_lst=[]
            if tags_div is not None:
                tags=tags_div.find_all('a')
                for tag in tags:
                    tag_lst.append(tag.text)
            tag_str=','.join(tag_lst)

            nba_news=NBANews(
                id_=news_id,
                title=title,
                pub_date=pub_date,
                source_name=source_name,
                source_author=source_author,
                source_category=source_category,
                cover_image_url=cover_image_url,
                cover_thumbnail_url=cover_thumbnail_url,
                cover_caption=cover_caption,
                content=contents,
                tags=tag_str
            )

            # 任務間轉換時需要JSON
            all_nba_news_dict.append(nba_news.__dict__)
    save_nba_news.delay(all_nba_news_dict)

@shared_task(name='save_nba_news')
def save_nba_news(all_nba_news_dict):
    for nba_news_dict in all_nba_news_dict:
        # 從JSON恢復成object
        nba_news=NBANews()
        nba_news.__dict__.update(nba_news_dict)
        nba_news.tag_str_to_list()

        with transaction.atomic():
            tag_objects = [Tags.objects.update_or_create(name=tag_name)[0] for tag_name in nba_news.tags]

            source_object, created = Sources.objects.update_or_create(
                name=nba_news.source_name,
                defaults={'author': nba_news.source_author, 'category': nba_news.source_category}
            )

            cover_object, cover_object_created = Covers.objects.update_or_create(
                id=nba_news.id,
                defaults={'caption': nba_news.cover_caption}
            )

            response = requests.get(nba_news.cover_image_url)
            if response.status_code == 200 and cover_object_created:
                cover_object.image.save(os.path.basename(f"{nba_news.id}.png"), ContentFile(response.content), save=True)

            response = requests.get(nba_news.cover_thumbnail_url)
            if response.status_code == 200 and cover_object_created:
                cover_object.thumbnail.save(os.path.basename(f"{nba_news.id}.png"), ContentFile(response.content), save=True)


            news_object, created = News.objects.get_or_create(
                news_id=nba_news.id,
                defaults={
                    'title': nba_news.title,
                    'content': nba_news.content,
                    'pub_date': nba_news.pub_date,
                    'sources': source_object,
                    'covers': cover_object
                }
            )

            news_object.tags.add(*tag_objects)

            print(f"Saved NBA news: {news_object.title}")
    # consumer=Consumer()
    # consumer.send_nba_news()

