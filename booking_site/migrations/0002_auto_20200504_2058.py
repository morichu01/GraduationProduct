# Generated by Django 3.0.5 on 2020-05-04 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book1',
            name='img_url',
            field=models.CharField(max_length=100, verbose_name='画像'),
        ),
        migrations.AlterField(
            model_name='book1',
            name='title',
            field=models.CharField(max_length=100, verbose_name='タイトル'),
        ),
    ]
