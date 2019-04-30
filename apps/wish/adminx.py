import xadmin
from .models import Wish, News


class WishAdmin(object):
    list_display = ['wxuser', 'content',"status","pv_num","up_num", "share_num","bb_num","end_time","add_time"]
    list_filter =['wxuser', 'content',"status","pv_num","up_num", "share_num","bb_num","end_time","add_time"]
    search_fields=['wxuser', 'content',"status","pv_num","up_num", "share_num","bb_num"]


class NewsAdmin(object):
    list_display = ['user', 'banner',"title","content","add_time"]
    list_filter =['user', 'banner',"title","content","add_time"]
    search_fields=['user', 'banner',"title","content"]


xadmin.site.register(Wish, WishAdmin)
xadmin.site.register(News, NewsAdmin)