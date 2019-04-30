from django.db import models
from datetime import datetime
from users.models import WxUsers
from wish.models import Wish
# Create your models here.


class Message(models.Model):
    """
    评论表，消息表
    """
    user_send=models.ForeignKey(WxUsers,on_delete=models.CASCADE,verbose_name='发出方',related_name='send')
    user_receive = models.ForeignKey(WxUsers, on_delete=models.CASCADE, verbose_name='接收方', related_name='receive')
    wish=models.ForeignKey(Wish,on_delete=models.CASCADE,verbose_name='被评论的愿望')
    parent_id=models.IntegerField(default=0,verbose_name='父级id')
    content = models.CharField(max_length=30, default='', verbose_name='内容', help_text='最多30字')
    images = models.CharField(max_length=2000, default='[]', verbose_name='内容', help_text='最多30字')
    is_read=models.BooleanField(default=False,verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name='评论表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.content


class Pick(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey(WxUsers, on_delete=models.CASCADE, verbose_name='点赞者')
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, verbose_name='被点赞的愿望')
    action=models.BooleanField(default=True,verbose_name='行为',help_text='true是点赞false是取消点赞')

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name='点赞表'
        verbose_name_plural=verbose_name


class Share(models.Model):
    """
    分享表
    """
    user = models.ForeignKey(WxUsers, on_delete=models.CASCADE, verbose_name='分享者')
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, verbose_name='被分享的愿望')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name='分享表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.user


class Notice(models.Model):
    """
    系统通知表（超越私信）
    """
    user_send=models.ForeignKey(WxUsers, default=None,on_delete=models.CASCADE, verbose_name='触发通知用户', related_name='notice_send')
    user_receive=models.ForeignKey(WxUsers, default=None, on_delete=models.CASCADE, verbose_name='接受通知用户', related_name='notice_receive')
    wish = models.ForeignKey(Wish, default=None, on_delete=models.CASCADE, verbose_name='动态')
    action = models.BigIntegerField(default=1 ,verbose_name='行为', help_text='1: 评论 2: 点赞')
    action_id = models.IntegerField(default=0, verbose_name='行为id', help_text='action 为1 评论ID， 2 点赞ID')
    content = models.CharField(default='', verbose_name='内容', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name='系统通知表'
        verbose_name_plural=verbose_name


class UserNotice(models.Model):
    """
    用户系统通知记录表
    """
    user=models.ForeignKey(WxUsers, default=None,on_delete=models.CASCADE, verbose_name='用户')
    last_read_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name='用户系统通知记录表'
        verbose_name_plural=verbose_name


class ShortMessages(models.Model):
    """
    短信息
    """
    user_send = models.ForeignKey(WxUsers, default=None, on_delete=models.CASCADE, verbose_name='发送信息用户',
                                  related_name='short_messages_send')
    user_receive = models.ForeignKey(WxUsers, default=None, on_delete=models.CASCADE, verbose_name='接受信息用户',
                                     related_name='short_messages_receive')
    content = models.CharField(default='', verbose_name='内容', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '信息表'
        verbose_name_plural = verbose_name


class UserShortMessages(models.Model):
    """
    用户系统通知记录表
    """
    user = models.ForeignKey(WxUsers, default=None, on_delete=models.CASCADE, verbose_name='用户')
    last_read_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '用户信息记录表'
        verbose_name_plural = verbose_name