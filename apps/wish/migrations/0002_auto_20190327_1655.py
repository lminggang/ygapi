# Generated by Django 2.0.5 on 2019-03-27 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodayTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today', models.CharField(default='', max_length=200, verbose_name='话题')),
            ],
            options={
                'verbose_name': '今日话题',
                'verbose_name_plural': '今日话题',
            },
        ),
        migrations.AddField(
            model_name='wish',
            name='is_false',
            field=models.BooleanField(default=0, verbose_name='假粉'),
        ),
        migrations.AddField(
            model_name='wish',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='话题'),
        ),
    ]
