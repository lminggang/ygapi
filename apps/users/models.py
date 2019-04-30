from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Create your models here.


class WxUsers(AbstractUser):
    """
    管理员
    """
    token=models.CharField(max_length=64,null=True,blank=True,verbose_name='token')
    nickName=models.CharField(max_length=30,null=True,blank=True,verbose_name='昵称')
    img_id = models.ImageField(max_length=200,upload_to='user_img/',blank=True,verbose_name='用户头像URL')
    images = models.CharField(max_length=200,default="",verbose_name='图片列表')
    sex = models.CharField(max_length=4, choices=(('0', '未知'),('1', '男'), ('2', '女')), default='0',
                              verbose_name='性别')
    province=models.CharField(max_length=20,null=True,blank=True,verbose_name='用户所在省')
    city=models.CharField(max_length=20,null=True,blank=True,verbose_name='用户所在市')
    country=models.CharField(max_length=20,null=True,blank=True,verbose_name='用户所在旗县区')
    longitude = models.FloatField(default=0,verbose_name="经度")
    latitude = models.FloatField(default=0,verbose_name="纬度")
    description = models.CharField(max_length=200,null=True,blank=True,verbose_name='描述')
    account_state = models.BooleanField(default='1',verbose_name='账户状态')
    phone_number = models.CharField(max_length=64,null=True,blank=True,verbose_name='电话号码')
    sign = models.IntegerField(default=0,verbose_name="签到")
    is_false = models.BooleanField(default='0',verbose_name='是否是僵尸粉')

    class Meta:
        verbose_name='管理员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class RegisterCode(models.Model):
    """
    注册码
    """
    code=models.CharField(max_length=20,default='',verbose_name='register_code')
    status=models.BooleanField(default=False,verbose_name='register_code_statud',help_text='1: use, 2: not use')
    add_time=add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name='注册码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
