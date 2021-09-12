from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, unique=True, blank=True)

    full_name = models.CharField(max_length=80)

    code = models.CharField(max_length=6, default=0, blank=True)

    avatar = models.ImageField(upload_to='images/', blank=False)
    cap = models.ImageField(upload_to='images/', blank=False)

    description = models.TextField(default='Нет описания пользователя.')
    two_factor = models.BooleanField(default=False)

    subscribers = models.ManyToManyField('self', related_name='followers', blank=False)
    subscriptions = models.ManyToManyField('self', related_name='followers', blank=False)

    newbie = models.BooleanField(default=True)

    date_of_creation = models.DateTimeField(auto_now=True)

    API_TOKEN = models.TextField(blank=False)

    @staticmethod
    def generate_auth_code():
        code = [str(random.choice(range(10))) for i in range(6)]
        return ''.join(code)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Pin(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    title = models.TextField()
    description = models.TextField()

    sourse = models.TextField()

    views = models.IntegerField(default=0)

    date_of_creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Board(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.TextField()
    cover = models.ImageField(upload_to='images/')
    pins = models.ManyToManyField(Pin)

    def __str__(self):
        return self.name


class Like(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)


class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)

    date_of_creation = models.DateTimeField(auto_now=True)


class Message(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    date_of_creation = models.TimeField(auto_now=True)


class PinMessage(Message):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)