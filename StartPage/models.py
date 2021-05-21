from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

RED = 'red'
GREEN = 'green'
ORANGE = 'orange'

COLOUR_STATUS_CHOICES = (
    (RED, 'red'),
    (GREEN, 'green'),
    (ORANGE, 'orange'),
)


class Book(models.Model):
    book = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class Vocabulary(models.Model):
    word = models.TextField()
    translation = models.TextField()
    status = models.DateTimeField(auto_now_add=True)
    colour_status = models.CharField(max_length=6, choices=COLOUR_STATUS_CHOICES, default=RED)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)




