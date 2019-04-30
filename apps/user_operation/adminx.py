import xadmin
from .models import Message,Pick,Share,Notice,ShortMessages


class MessageAdmin(object):
    list_display = ['user_send', 'user_receive',"wish","content","is_read","add_time"]
    list_filter =['user_send', 'user_receive',"wish","content","is_read","add_time"]
    search_fields=['user_send', 'user_receive',"wish","content","is_read"]


class PickAdmin(object):
    list_display = ['user', 'wish',"action","add_time"]
    list_filter =['user', 'wish',"action","add_time"]
    search_fields=['user', 'wish']


class ShareAdmin(object):
    list_display = ['user', 'wish',"add_time"]
    list_filter =['user', 'wish',"add_time"]
    search_fields=['user', 'wish']


class NoticeAdmin(object):
    list_display = ['admin', 'content',"add_time"]
    list_filter =['admin', 'content',"add_time"]
    search_fields=['admin', 'content']

class ShortMessagesAdmin(object):
    list_display = ['admin', 'content', "add_time"]
    list_filter = ['admin', 'content', "add_time"]
    search_fields = ['admin', 'content']


xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(Pick, PickAdmin)
xadmin.site.register(Share, ShareAdmin)
xadmin.site.register(Notice, NoticeAdmin)
xadmin.site.register(ShortMessages, ShortMessagesAdmin)