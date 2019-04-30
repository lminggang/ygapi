# Generated by Django 2.0.5 on 2019-04-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish', '0003_wish_lld'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='bb_num',
            field=models.IntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='图片列表'),
        ),
        migrations.AddField(
            model_name='news',
            name='latitude',
            field=models.FloatField(default=0, verbose_name='纬度'),
        ),
        migrations.AddField(
            model_name='news',
            name='longitude',
            field=models.FloatField(default=0, verbose_name='经度'),
        ),
        migrations.AddField(
            model_name='news',
            name='pv_num',
            field=models.IntegerField(default=0, verbose_name='浏览数'),
        ),
        migrations.AddField(
            model_name='news',
            name='share_num',
            field=models.IntegerField(default=0, verbose_name='转发数'),
        ),
        migrations.AddField(
            model_name='news',
            name='up_num',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='wish',
            name='images',
            field=models.CharField(default='', max_length=200, verbose_name='动态图片列表'),
        ),
        migrations.AlterField(
            model_name='news',
            name='banner',
            field=models.ImageField(blank=True, max_length=200, upload_to='banner/', verbose_name='轮播图'),
        ),
    ]