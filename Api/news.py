import math
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile 
from django.conf import settings

from users.models import *
from user_operation.models import *
from wish.models import *
from Api.resources import Resource
from Api.utils import *
from django.http.response import HttpResponse
from Api.decorators import *

class GetNewsList(Resource):
    def get(self,request, *args, **kwargs):
        data = request.GET
        limit = abs(int(data.get('limit', 5)))
        start_id = data.get('start_id', False)
        page = abs(int(data.get('page', 1)))

        news = []
        if start_id:
            start_id = int(start_id)
        else:
            start_id = 0
        news.append(Q(id__gt=start_id))

        if limit > 10:
            limit = 10
        all_objs = News.objects.filter(*news)
        pages = math.ceil(all_objs.count()/limit) or 1
        if page > pages:
            page = pages
        start = (page-1)*limit
        end = page*limit
        objs = all_objs[start:end]
        data = []
        # comment = []
        for obj in objs:
            obj_dict = dict()
            obj_dict['id'] = obj.id
            id = obj_dict['id']
            # wish_user = obj.wxuser
            # Pick_user = Pick.objects.filter(wish__id=obj.id)
            # if user.is_authenticated:
            #     if Pick_user.count():
            #         pick = Pick_user.filter(user__id=user.id)
            #         if pick.count():
            #             if Pick_user.get(user__id=user.id).action:
            #                 obj_dict['is_pick'] = 1
            #             else:
            #                 obj_dict['is_pick'] = 0
            #         else:
            #             obj_dict['is_pick'] = 0
            #     else:
            #         obj_dict['is_pick'] = 0
            # else:
            #     obj_dict['is_pick'] = 0
            # obj_dict['username']= wish_user.username
            # obj_dict['username_sex'] =wish_user.sex
            # obj_dict['user_imgid'] = str(wish_user.img_id)
            # obj_dict['content'] = obj.content
            obj_dict['title'] = obj.title
            obj_dict['add_time'] = datetime.strftime(obj.add_time, "%Y-%m-%d %H:%M:%S")
            # obj_dict['viewcount'] = obj.pv_num
            # obj_dict['praiseid'] = obj.up_num
            # obj_dict['shareid'] = obj.share_num
            # obj_dict['comment_num'] = obj.bb_num
            obj_dict['longitude'] = obj.longitude
            obj_dict['latitude'] = obj.latitude
            # obj_dict['order_by'] = obj.order_by
            obj_dict['images'] = obj.image
            # messages = Message.objects.filter(wish__id=obj.id)
            # for message in messages:
            #     message_dict = dict()
            #     message_dict["username"] = message.user_send.username
            #     message_dict["comment"]  = message.content
            #     comment.append(message_dict)
            # obj_dict['comment'] = comment
            data.append(obj_dict)
        return json_response({
            "page":page,
            'objs': data
        })


class GetNewsInfo(Resource):
    """获取单条新闻"""
    def post(self, request,*args,**kwargs):
        data = request.POST
        newsid = data.get('newsid','')
        if not newsid:
            return json_response({
                "msg":"newsid不能为空"
            })
        obj_dict = dict()
        obj = News.objects.get(id=newsid)
        obj_dict['title'] = obj.title
        obj_dict['content'] = obj.content
        obj_dict['images'] = obj.image
        obj_dict['add_time'] = datetime.strftime(obj.add_time, "%Y-%m-%d %H:%M:%S")
        obj_dict['longitude'] = obj.longitude
        obj_dict['latitude'] = obj.latitude        
        return json_response({
            "data":obj_dict
        })