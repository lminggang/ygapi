# Generated by Django 2.0.5 on 2019-03-27 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wish', '0002_auto_20190327_1655'),
        ('user_operation', '0002_auto_20190321_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='action',
            field=models.BigIntegerField(default=1, help_text='1: 评论 2: 点赞', verbose_name='行为'),
        ),
        migrations.AddField(
            model_name='notice',
            name='user_receive',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='notice_receive', to=settings.AUTH_USER_MODEL, verbose_name='接受通知用户'),
        ),
        migrations.AddField(
            model_name='notice',
            name='user_send',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='notice_send', to=settings.AUTH_USER_MODEL, verbose_name='触发通知用户'),
        ),
        migrations.AddField(
            model_name='notice',
            name='wish',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='wish.Wish', verbose_name='动态'),
        ),
    ]
