# coding: utf8

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=128)
    create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class Comment(models.Model):
    aid = models.IntegerField(default=0)  # Article_id 做关联
    name = models.CharField(max_length=128)
    create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
