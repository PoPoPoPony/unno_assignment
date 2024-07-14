from django.db import models

class News(models.Model):
    news_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField()
    tags = models.ManyToManyField('Tags', related_name='news')
    sources = models.ForeignKey('Sources', on_delete=models.SET_NULL, null=True)
    covers = models.OneToOneField('Covers', on_delete=models.SET_NULL, related_name='news', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Covers(models.Model):
    caption = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    image = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.caption

class Sources(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
