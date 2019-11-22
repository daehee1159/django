from django.db import models

# Create your models here.

# import된 models.Model을 매개변수로 받고 클래스안에 제목,날짜,내용으로 구성
class Blog(models.Model):
    # CharField -> 문자로 구성되어 있는 항목
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()