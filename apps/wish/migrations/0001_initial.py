# Generated by Django 2.0.5 on 2019-03-21 19:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=200, upload_to='images/')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '新闻图片',
                'verbose_name_plural': '新闻图片',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(max_length=200, upload_to='banner/', verbose_name='轮播图')),
                ('title', models.CharField(default='', help_text='最多15字', max_length=15, verbose_name='新闻标题')),
                ('content', models.CharField(default='', help_text='最多800字', max_length=800, verbose_name='新闻正文')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '新闻表',
                'verbose_name_plural': '新闻表',
            },
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', help_text='最多200字', max_length=200, verbose_name='动态内容')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('pv_num', models.IntegerField(default=0, verbose_name='浏览数')),
                ('up_num', models.IntegerField(default=0, verbose_name='点赞数')),
                ('share_num', models.IntegerField(default=0, verbose_name='转发数')),
                ('bb_num', models.IntegerField(default=0, verbose_name='评论数')),
                ('order_by', models.IntegerField(default=0, verbose_name='排序号')),
                ('img_id', models.ImageField(blank=True, max_length=200, upload_to='wish_img/', verbose_name='动态的图片')),
                ('longitude', models.FloatField(default=0, verbose_name='经度')),
                ('latitude', models.FloatField(default=0, verbose_name='纬度')),
                ('is_delete', models.BooleanField(default=0, verbose_name='是否删除')),
                ('wxuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '动态信息表',
                'verbose_name_plural': '动态信息表',
            },
        ),
        migrations.AddField(
            model_name='images',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wish.News', verbose_name='新闻'),
        ),
    ]