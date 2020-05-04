from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(
        verbose_name='タイトル',
        max_length=50,
    )

    thumbnail = models.ImageField(
        verbose_name='サムネイル',
        upload_to="thumbnails/",
    )

    booklog_id = models.CharField(
        verbose_name='サイトid',
        max_length=10,
      )


class Book1(models.Model):
    title = models.CharField(
        verbose_name='タイトル',
        max_length=150
    )

    img_url = models.CharField(
        verbose_name='画像',
        max_length=100
    )

    no = models.CharField(
        verbose_name='アイテムNo',
        max_length=10
    )


class Borrow(models.Model):
    title = models.ForeignKey(
        Book1,
        verbose_name='タイトル',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        verbose_name='名前',
        on_delete=models.CASCADE,
    )

    start = models.DateField(
        verbose_name='開始時間',
        default=timezone.now,
    )

    end = models.DateField(
        verbose_name='終了時間',
        default=timezone.now,
    )

