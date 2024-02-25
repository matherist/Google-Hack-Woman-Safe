from django.db import models
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup


class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)