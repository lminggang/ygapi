# Generated by Django 2.0.5 on 2019-04-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxusers',
            name='images',
            field=models.CharField(default='', max_length=200, verbose_name='图片列表'),
        ),
        migrations.AddField(
            model_name='wxusers',
            name='is_false',
            field=models.BooleanField(default='0', verbose_name='是否是僵尸粉'),
        ),
    ]
