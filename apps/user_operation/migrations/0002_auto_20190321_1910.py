# Generated by Django 2.0.5 on 2019-03-21 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_operation', '0001_initial'),
        ('wish', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='分享者'),
        ),
        migrations.AddField(
            model_name='share',
            name='wish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wish.Wish', verbose_name='被分享的愿望'),
        ),
        migrations.AddField(
            model_name='pick',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者'),
        ),
        migrations.AddField(
            model_name='pick',
            name='wish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wish.Wish', verbose_name='被点赞的愿望'),
        ),
        migrations.AddField(
            model_name='notice',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='user_receive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive', to=settings.AUTH_USER_MODEL, verbose_name='接收方'),
        ),
        migrations.AddField(
            model_name='message',
            name='user_send',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send', to=settings.AUTH_USER_MODEL, verbose_name='发出方'),
        ),
        migrations.AddField(
            model_name='message',
            name='wish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wish.Wish', verbose_name='被评论的愿望'),
        ),
    ]
