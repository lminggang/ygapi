from django.db import models
from users.models import WxUsers
from datetime import datetime
from django.utils.safestring import mark_safe
# Create your models here.


class Wish(models.Model):
    """
    动态信息表
    """
    wxuser=models.ForeignKey(WxUsers,on_delete=models.CASCADE)
    content=models.CharField(max_length=200,default='',verbose_name='动态内容',help_text='最多200字')
    title = models.CharField(max_length=200,default='',verbose_name='话题')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    pv_num=models.IntegerField(default=0,verbose_name='浏览数')
    up_num=models.IntegerField(default=0,verbose_name='点赞数')
    share_num=models.IntegerField(default=0,verbose_name='转发数')
    bb_num=models.IntegerField(default=0,verbose_name='评论数')
    order_by = models.IntegerField(default=0,verbose_name='排序号')
    img_id = models.ImageField(max_length=200,upload_to='wish_img/',blank=True,verbose_name='动态的图片')
    images = models.CharField(max_length=200,default="",verbose_name='动态图片列表')
    longitude =models.FloatField(default=0,verbose_name="经度")
    latitude =models.FloatField(default=0,verbose_name="纬度")
    is_delete = models.BooleanField(default=0,verbose_name='是否删除')
    is_false = models.BooleanField(default=0,verbose_name="假粉")
    lld = models.BooleanField(default=1,verbose_name="凉凉度",help_text='为0表示不再出现')

    class Meta:
        verbose_name='动态信息表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.content

class TodayTitle(models.Model):
    """
    今日话题
    """
    today = models.CharField(max_length=200,default='',verbose_name='话题')

    class Meta:
        verbose_name='今日话题'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.today

class News(models.Model):
    """
    新闻表
    """
    user=models.ForeignKey(WxUsers,on_delete=models.CASCADE)
    banner=models.ImageField(max_length=200,blank=True,upload_to='banner/',verbose_name='轮播图')
    image = models.CharField(max_length=200,default='',blank=True,verbose_name='图片列表')
    title=models.CharField(max_length=15,default='',verbose_name='新闻标题',help_text='最多15字')
    content=models.CharField(max_length=800,default='',verbose_name='新闻正文',help_text='最多800字')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    pv_num=models.IntegerField(default=0,verbose_name='浏览数')
    up_num=models.IntegerField(default=0,verbose_name='点赞数')
    share_num=models.IntegerField(default=0,verbose_name='转发数')
    bb_num=models.IntegerField(default=0,verbose_name='评论数')
    longitude =models.FloatField(default=0,verbose_name="经度")
    latitude =models.FloatField(default=0,verbose_name="纬度")

    class Meta:
        verbose_name='新闻表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

    def image_url(self):
        return mark_safe('<img src="/media/{0}" class="field_img">'.format(self.banner))

    image_url.short_description = '轮播图'


class Images(models.Model):
    """
    新闻图片
    """
    image = models.ImageField(max_length=200, upload_to='images/')
    news=models.ForeignKey(News, verbose_name="新闻", blank=True,null=True,on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "新闻图片"
        verbose_name_plural = verbose_name

    def image_url(self):
        return mark_safe('<img src="/media/{0}" class="field_img">'.format(self.image))

    image_url.short_description = '图片'