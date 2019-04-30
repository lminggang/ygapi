from django.conf.urls import url

from Api.user_operate import *
from Api.user_action import *
from Api.upload import *
from Api.messages import *
from Api.news import *
from Api.register_code import *
from Api.resources import Register

api = Register()
# 通用接口
api.regist(my_wish('my_wish'))
api.regist(get_wish('get_wish'))
api.regist(regist('regist'))
api.regist(SessionResource('session'))
api.regist(get_wish_info('get_wish_info'))

# comment api path
api.regist(add_comment('add_comment'))
api.regist(del_comment('del_comment'))
api.regist(get_comment_list('get_comment_list'))
api.regist(get_user_comment_list('get_user_comment_list'))

# pick api path
api.regist(add_pick('add_pick'))
api.regist(del_pick('del_pick'))
api.regist(get_user_pick_list('get_user_pick_list'))

# share api path
api.regist(add_share('add_share'))

# 获取今题话题
api.regist(today_title("today_title"))

# 地图相关
api.regist(map("map"))

# notice api path
api.regist(notice('get_user_notice_list'))
api.regist(get_new_notice_count('get_new_notice_count'))

# 流星雨接口
api.regist(meteor('meteor'))

# upload api path
api.regist(upload_images('upload_images'))

# short messages api path
api.regist(AddShortMessages('add_short_messages'))
api.regist(GetShortMessagesList('get_short_messages_list'))
api.regist(GetUserNewShortMessages('get_user_new_short_messages'))

# 新闻接口
api.regist(GetNewsList('getnewslist'))
api.regist(GetNewsInfo('getnewsinfo'))

# register_code api path
api.regist(GenerateRegisterCode('code_rg'))

# 联系人接口
api.regist(Linkman('linkman'))