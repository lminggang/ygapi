import random
import json
import time
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
#from django.conf import settings
from Api.falsewish import FALSEWISH

from users.models import *
from user_operation.models import *
from wish.models import *
from Api.resources import Resource
from Api.utils import *
from django.http.response import HttpResponse
from Api.decorators import *

class today_title(Resource):
    # 获取今日话题
    @userinfo_required
    def get(self,request,*args,**kwargs):
        obj = TodayTitle.objects.last()
        if not obj:
            return json_response({
                "msg":"没有任何话题"
            })
        today = obj.today
        return json_response({
            "today_title":today
        })

    # 获取今日话题的动态
    @userinfo_required
    def post(self,request,*args,**kwargs):
        data = request.POST
        user = request.user
        today_title = data.get('today_title','')
        if not today_title:
            return json_response({
                "msg":"今题话题不能为空"
            })
        all_objs = Wish.objects.filter(title = today_title, is_delete=False)
        if not all_objs.count():
            return json_response({
                "msg":"没有找到关于这个话题的动态"
            })
        data = []
        comment = []
        for obj in all_objs:
            obj_dict = dict()
            obj_dict['id'] = obj.id
            wish_user = obj.wxuser
            Pick_user = Pick.objects.filter(wish__id=obj.id)
            if Pick_user.count():
                pick = Pick_user.filter(user__id=user.id)
                if pick.count():
                    if Pick_user.get(user__id=user.id).action:
                        obj_dict['is_pick'] = 1
                    else:
                        obj_dict['is_pick'] = 0
                else:
                    obj_dict['is_pick'] = 0
            else:
                obj_dict['is_pick'] = 0
            obj_dict['username']= wish_user.username
            obj_dict['username_sex'] =wish_user.sex
            obj_dict['images'] = wish_user.images
            obj_dict['title'] = obj.title
            obj_dict['content'] = obj.content
            obj_dict['add_time'] = datetime.strftime(obj.add_time, "%Y-%m-%d %H:%M:%S")
            obj_dict['viewcount'] = obj.pv_num
            obj_dict['praiseid'] = obj.up_num
            obj_dict['shareid'] = obj.share_num
            obj_dict['comment_num'] = obj.bb_num
            obj_dict['longitude'] = obj.longitude
            obj_dict['latitude'] = obj.latitude
            obj_dict['order_by'] = obj.order_by
            obj_dict['images'] = obj.images
            messages = Message.objects.filter(wish__id=obj.id)
            for message in messages:
                message_dict = dict()
                message_dict["username"] = message.user_send.username
                message_dict["comment"]  = message.content
                comment.append(message_dict)
            obj_dict['comment'] = comment
            data.append(obj_dict)
        return json_response({
            'objs': data
        })

class map(Resource):
    # 获取指定经纬度的动态
    def post(self,request,*args,**kwargs):
        user = request.user
        data = request.POST
        longitude = float(data.get('longitude',0))
        latitude = float(data.get('latitude',0))
        data = []
        if not (longitude and latitude):
            return json_response({
                "msg":"经纬度不能为空"
            })
        all_objs = Wish.objects.filter(longitude__gt = longitude - 0.5,longitude__lt= longitude + 0.5, latitude__gt= latitude-0.5 , latitude__lt =  latitude + 0.5 ,is_delete=False)
        if not all_objs.count():
            a1=(2019,3,20,0,0,0,0,0,0)              #设置开始日期时间元组（1976-01-01 00：00：00）
            a2=(2019,4,5,23,59,59,0,0,0)    #设置结束日期时间元组（1990-12-31 23：59：59）
            start=time.mktime(a1)    #生成开始时间戳
            end=time.mktime(a2)  
            t=random.randint(start,end)    #在开始和结束时间戳中随机取出一个
            date_touple=time.localtime(t) 
            random_num = random.randint(1,10) 
            if random_num <= 6:
                random_num = 1  
            elif 6 < random_num <= 9:
                random_num = 2
            elif random_num == 10:
                random_num = 3
            for obj in range(random_num):
                obj_dict = dict()
                obj_dict = FALSEWISH[random.randint(0,1902)]
                username = obj_dict["user"]
                exist = WxUsers.objects.filter(username=username).count()
                if not exist:
                    with atomic():
                        user = WxUsers()
                        user.username = username
                        user.set_password("12345")
                        user.sex = random.randint(1,2)
                        user.is_false = 1
                        user.save()
                else:
                    user = WxUsers.objects.get(username=username)
                with atomic():
                    wish = Wish()
                    wish.wxuser_id = user.id
                    wish.content = obj_dict["content"]
                    wish.longitude = round(longitude + random.uniform(-0.4, 0.4),6)
                    wish.latitude = round(latitude + random.uniform(-0.4, 0.4),6)
                    wish.add_time = time.strftime("%Y-%m-%d %H:%M:%S",date_touple)
                    wish.is_false = 1
                    wish.save()
            time.sleep(0.1)
        all_objs = Wish.objects.filter(longitude__gt = longitude - 0.5,longitude__lt= longitude + 0.5, latitude__gt= latitude-0.5 , latitude__lt =  latitude + 0.5 ,is_delete=False)
        if not all_objs.count():
            return json_response({
                "msg":"数据丢失,请联系麻酱猫"
            })
        for obj in all_objs:
            obj_dict = dict()
            obj_dict['id'] = obj.id
            wish_user = obj.wxuser
            Pick_user = Pick.objects.filter(wish__id=obj.id)
            if user.is_authenticated:
                if Pick_user.count():
                    pick = Pick_user.filter(user__id=user.id)
                    if pick.count():
                        if Pick_user.get(user__id=user.id).action:
                            obj_dict['is_pick'] = 1
                            obj_dict['pick_id'] = Pick_user.get(user__id=user.id).id
                        else:
                            obj_dict['is_pick'] = 0
                    else:
                        obj_dict['is_pick'] = 0
                else:
                    obj_dict['is_pick'] = 0
            else:
                obj_dict['is_pick'] = 0
            obj_dict['wishuser_id']= wish_user.id
            obj_dict['username']= wish_user.username
            obj_dict['nickName'] = wish_user.nickName
            obj_dict['username_sex'] =wish_user.sex
            obj_dict['images'] = wish_user.images
            obj_dict['title'] = obj.title
            obj_dict['images'] = obj.images
            obj_dict['content'] = obj.content
            obj_dict['add_time'] = datetime.strftime(obj.add_time, "%Y-%m-%d %H:%M:%S")
            obj_dict['viewcount'] = obj.pv_num
            obj_dict['praiseid'] = obj.up_num
            obj_dict['shareid'] = obj.share_num
            obj_dict['comment_num'] = obj.bb_num
            obj_dict['longitude'] = obj.longitude
            obj_dict['latitude'] = obj.latitude
            obj_dict['order_by'] = obj.order_by
            obj_dict['is_false'] = obj.is_false
            messages = Message.objects.filter(wish__id=obj.id)
            comment = []
            for message in messages:
                message_dict = dict()
                message_dict["message_id"] = message.id
                message_dict["username"] = message.user_send.username
                message_dict["comment"]  = message.content
                message_dict["parent_id"] = message.parent_id
                message_dict["comment_images"] = message.images.replace('"','')
                # print(r(message.images))
                comment.append(message_dict)
            obj_dict['comment'] = comment
            data.append(obj_dict)
        return json_response({
                'objs': data
        })

class my_wish(Resource):
    # 获取我的动态
    @userinfo_required
    def get(self, request, *args, **kwargs):
        user = request.user
        data = request.GET
        limit = abs(int(data.get('limit', 5)))
        start_id = data.get('start_id', False)
        page = abs(int(data.get('page', 1)))
        Wishes = []
        if start_id:
            start_id = int(start_id)
        else:
            start_id = 0
        Wishes.append(Q(id__gt=start_id))

        if limit > 10:
            limit = 10
        Wishes.append(Q(wxuser_id=request.user.id,is_delete=False))

        all_objs = Wish.objects.filter(*Wishes)
        pages = math.ceil(all_objs.count()/limit) or 1
        if page > pages:
            page = pages
        start = (page-1)*limit
        end = page*limit
        objs = all_objs[start:end]

        data = []
        for obj in objs:
            obj_dict = dict()
            obj_dict['id'] = obj.id
            obj_dict['username'] = user.username
            obj_dict['title'] = obj.title
            obj_dict['content'] = obj.content
            obj_dict['add_time'] = datetime.strftime(obj.add_time, "%Y-%m-%d %H:%M:%S")
            obj_dict['viewcount'] = obj.pv_num
            obj_dict['praiseid'] = obj.up_num
            obj_dict['shareid'] = obj.share_num
            obj_dict['comment_num'] = obj.bb_num
            obj_dict['longitude'] = obj.longitude
            obj_dict['latitude'] = obj.latitude
            obj_dict['order_by'] = obj.order_by
            obj_dict['images'] = obj.images
            messages = Message.objects.filter(wish__id=obj.id)
            comment = []
            for message in messages:
                message_dict = dict()
                message_dict["message_id"] = message.id
                message_dict["username"] = message.user_send.username
                message_dict["comment"]  = message.content
                message_dict["parent_id"] = message.parent_id
                message_dict["comment_images"] = message.images.replace('"','')
                # print(r(message.images))
                comment.append(message_dict)
            obj_dict['comment'] = comment
            data.append(obj_dict)
        return json_response({
            "page":page,
            'objs': data})
    
    # 删除动态
    @atomic
    @userinfo_required
    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            data = request.DELETE
            if not data:
                return json_response({
                    "msg":"请求数据类型不正确"
                })
            id = data.get('id', [])
            #objs = Wish.objects.filter(id__in=ids, user=request.user.id, state__in=[0, 2, 3])
            objs = Wish.objects.filter(id__in=id,wxuser_id=request.user.id, is_delete=False)
            deleted_ids = [obj.id for obj in objs]
            objs.delete()
            return json_response({
                'deleted_id': deleted_ids
            })
    # 发布动态
    @atomic
    @userinfo_required
    def post(self, request, *args, **kwargs):
        data = request.POST
        if not data:
            return json_response({
                "msg":"请求数据类型不正确"
            })
        img = request.FILES.get("img", default="")
        wish = Wish()
        wish.wxuser_id = request.user.id
        wish.title = data.get('title','')
        wish.content = data.get('content', '内容')
        wish.longitude = data.get('longitude',0)
        wish.latitude = data.get('latitude',0)
        wish.images = data.get('images',"")
        wish.save()
        return json_response({
            "id": wish.id
        })

class get_wish(Resource):
    # 获取所有人的动态
    def get(self,request, *args, **kwargs):
        data = request.GET
        user = request.user
        limit = abs(int(data.get('limit', 5)))
        start_id = data.get('start_id', False)
        page = abs(int(data.get('page', 1)))

        Wishes = []
        if start_id:
            start_id = int(start_id)
        else:
            start_id = 0
        Wishes.append(Q(id__gt=start_id))

        if limit > 10:
            limit = 10
        all_objs = Wish.objects.filter(*Wishes)
        pages = math.ceil(all_objs.count()/limit) or 1
        if page > pages:
            page = pages
        start = (page-1)*limit
        end = page*limit
        objs = all_objs[start:end]
        data = []
        for obj in objs:
            obj_dict = dict()
            obj_dict['id'] = obj.id
            id = obj_dict['id']
            wish_user = obj.wxuser
            Pick_user = Pick.objects.filter(wish__id=obj.id)
            if user.is_authenticated:
                if Pick_user.count():
                    pick = Pick_user.filter(user__id=user.id)
                    if pick.count():
                        if Pick_user.get(user__id=user.id).action:
                            obj_dict['is_pick'] = 1
                        else:
                            obj_dict['is_pick'] = 0
                    else:
                        obj_dict['is_pick'] = 0
                else:
                    obj_dict['is_pick'] = 0
            else:
                obj_dict['is_pick'] = 0
            obj_dict['username']= wish_user.username
            obj_dict['username_sex'] =wish_user.sex
            obj_dict['user_imgid'] = wish_user.images
            obj_dict['content'] = obj.content
            obj_dict['title'] = obj.title
            obj_dict['add_time'] = datetime.strftime(obj.add_time, "%Y-%m-%d %H:%M:%S")
            obj_dict['viewcount'] = obj.pv_num
            obj_dict['praiseid'] = obj.up_num
            obj_dict['shareid'] = obj.share_num
            obj_dict['comment_num'] = obj.bb_num
            obj_dict['longitude'] = obj.longitude
            obj_dict['latitude'] = obj.latitude
            obj_dict['order_by'] = obj.order_by
            obj_dict['images'] = obj.images
            messages = Message.objects.filter(wish__id=obj.id)
            comment = []
            for message in messages:
                message_dict = dict()
                message_dict["message_id"] = message.id
                message_dict["username"] = message.user_send.username
                message_dict["comment"]  = message.content
                message_dict["parent_id"] = message.parent_id
                message_dict["comment_images"] = message.images.replace('"','')
                # print(r(message.images))
                comment.append(message_dict)
            obj_dict['comment'] = comment
            data.append(obj_dict)
        return json_response({
            "page":page,
            'objs': data
        })

# 用户登录与退出
class SessionResource(Resource):
    # 获取登陆状态
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return json_response({
                'msg': '已经登录',
                "username":request.user.username
            })
        return not_authenticated()

    # 登陆
    def put(self, request, *args, **kwargs):
        data = request.PUT
        if not data:
            return json_response({
                "msg":"请求数据类型不正确"
            })
        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return json_response({
                'msg': '登录成功',
                "id" : user.id,
                "username": user.username,
                "nickName": user.nickName,
                "images": user.images
            })
        return params_error({
            'msg': '用户名或密码错误'
        })

    # 退出
    def delete(self, request, *args, **kwargs):
        logout(request)
        return json_response({
            'msg': '退出成功'
        })

class regist(Resource):
    def post(self,request, *args, **kwargs):
        data = request.POST
        if not data:
            return json_response({
                "msg":"请求数据类型不正确"
            })
        img = request.FILES.get("img", default="")
        username = data.get('username', '')
        exist = WxUsers.objects.filter(username=username).count()
        if exist:
            return json_response({
                    "msg": "用户名已存在"
                })
        password = data.get('password', '')
        regist_code = data.get('regist_code', '')
        nickName = data.get('nickname','')
        sex = data.get('sex','0')
        province = data.get('province','')
        city = data.get('city','')
        country = data.get('contry','')
        longitude = data.get('longitude',0)
        latitude = data.get('latitude',0)
        description = data.get('description','')
        phone_number = data.get('phone_number','')
        images = data.get('images','')
        try:
            registcode = RegisterCode.objects.get(code=regist_code)
        except Exception as e:
            return json_response({
                "msg":"注册码不存在"
            })
        if registcode.status:
            return json_response({
                "msg":"注册码已被使用"
                })
        with atomic():
            user = WxUsers()
            user.username = username
            user.set_password(password)
            user.nickName = nickName
            user.sex = sex
            user.province = province
            user.country = country
            user.longitude = longitude
            user.latitude = latitude
            user.description = description
            user.phone_number = phone_number
            user.images = images
            registcode.status = True
            registcode.save()
            user.save()
            login(request, user)
            return json_response({
                "id": user.id,
                 "username": user.username,
                 "nickName": user.nickName
            })

class meteor(Resource):
    @userinfo_required
    def get(self,request,*args,**kwargs):
        # 凉凉度 = 8+2*（发布日期-抽取日期）-1*赞数量-3*评论数量+字符数量*1.5 ±10（同性别-10，异性+10）
        user = request.user
        Wishes = Wish.objects.filter(lld=1)
        if not Wishes.count():
            wishes_tmp = Wish.objects.all().update(lld=1)
            Wishes = Wish.objects.filter(lld=1)
        nowtime = datetime.now()
        dic = dict()
        for wish in Wishes:
        # 时间差,单位是天，向上取整
            time0 = (nowtime-wish.add_time).total_seconds()
            _time = math.ceil(float(time0)/86400)
            _lld = 8 + 2 * _time - 1 * wish.up_num - 3 * wish.bb_num + len(wish.content) * 1.5
            if wish.wxuser.sex  == user.sex:
                lld = _lld - 10
            else:
                lld = _lld + 10
            dic[wish.id] = lld
        id = sorted(dic.items(),key = lambda x:x[1],reverse = True)[0][0]
        return_wish = Wish.objects.get(id=id)
        return_wish.lld = 0
        return_wish.save()
        comment = []
        obj_dict = dict()
        obj_dict['id'] = return_wish.id
        wish_user = return_wish.wxuser
        Pick_user = Pick.objects.filter(wish__id=id)
        if Pick_user.count():
            pick = Pick_user.filter(user__id=user.id)
            if pick.count():
                if Pick_user.get(user__id=user.id).action:
                    obj_dict['is_pick'] = 1
                else:
                    obj_dict['is_pick'] = 0
            else:
                obj_dict['is_pick'] = 0
        else:
            obj_dict['is_pick'] = 0
        obj_dict['username']= wish_user.username
        obj_dict['username_sex'] =wish_user.sex
        obj_dict['user_imgid'] = wish_user.images
        obj_dict['content'] = return_wish.content
        obj_dict['title'] = return_wish.title
        obj_dict['add_time'] = datetime.strftime(return_wish.add_time, "%Y-%m-%d %H:%M:%S")
        obj_dict['viewcount'] = return_wish.pv_num
        obj_dict['praiseid'] = return_wish.up_num
        obj_dict['shareid'] = return_wish.share_num
        obj_dict['comment_num'] = return_wish.bb_num
        obj_dict['longitude'] = return_wish.longitude
        obj_dict['latitude'] = return_wish.latitude
        obj_dict['order_by'] = return_wish.order_by
        obj_dict['images'] = return_wish.images
        messages = Message.objects.filter(wish__id=return_wish.id)
        for message in messages:
            message_dict = dict()
            message_dict["username"] = message.user_send.username
            message_dict["comment"]  = message.content
            comment.append(message_dict)
        obj_dict['comment'] = comment
        return json_response({
            "data":obj_dict
        })

class get_wish_info(Resource):
    def get(self, request, *args, **kwargs):
        data = request.GET
        wish_id = data.get('wish_id', 0)
        # check params
        if not wish_id:
            return params_error()
        wish = Wish.objects.filter(id=wish_id)
        if not wish:
            return params_error()
        # serializers action
        result = json.loads(serializers.serialize('json', wish))
        result = [row['fields'] for row in result]
        return json_response(result)