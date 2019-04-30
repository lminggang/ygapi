import json
import datetime as dt
from datetime import datetime
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q

from users.models import *
from user_operation.models import *
from wish.models import *

from Api.resources import Resource
from Api.decorators import *


# add short messages
class AddShortMessages(Resource):
    def get(self, request, *args, **kwargs):
        return self.add_short_messages(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.add_short_messages(request.POST)

    def add_short_messages(self, data):
        user_send_id = data.get('send_user_id', 0)
        user_receive_id = data.get('receive_user_id', 0)
        content = data.get('content', '')
        if not user_send_id or \
            not user_receive_id or \
            not content or \
            len(content) > 30:
            return params_error()

        s_m = ShortMessages()
        s_m.user_send_id = user_send_id
        s_m.user_receive_id = user_receive_id
        s_m.content = content
        s_m.add_time = datetime.now()
        s_m.save()

        try:
            user_short_messages = UserShortMessages.objects.get(user_id=user_receive_id)
        except Exception as e:
            user_short_messages = UserShortMessages()
            user_short_messages.user_id = user_receive_id
            user_short_messages.last_read_time = datetime.now() - dt.timedelta(days=1000)
            user_short_messages.save()

        return json_response({'short_message_id': s_m.id, 'content': s_m.content})


class GetUserNewShortMessages(Resource):
    def get(self, request, *args, **kwargs):
        return self.get_user_short_messages_count(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.get_user_short_messages_count(request.POST)

    def get_user_short_messages_count(self, data):
        # check params
        user_id = data.get('user_id', 0)
        if not user_id:
            return params_error()

        try:
            try:
                user_short_messages = UserShortMessages.objects.get(user_id=user_id)
            except Exception as e:
                user_short_messages = UserShortMessages()
                user_short_messages.user_id = user_id
                user_short_messages.last_read_time = datetime.now()
                user_short_messages.save()
        except Exception as e:
            return params_error()

        short_messages_users = ShortMessages.objects.\
                                filter(user_receive_id=user_id,add_time__gt=user_short_messages.last_read_time).\
                                values('user_send_id').annotate(count=Count('user_send_id'))

        result = list()
        for smu in short_messages_users:
            result_dict = dict()
            sm_list = ShortMessages.objects.filter(user_send_id=smu.get('user_send_id'), user_receive_id=user_id, add_time__gt=user_short_messages.last_read_time).order_by('-id')
            try:
                user = WxUsers.objects.get(id=smu.get('user_send_id'))
            except Exception as e:
                return params_error()

            result_dict[smu.get('user_send_id')] = dict()
            result_dict[smu.get('user_send_id')]['user_id'] = user.id
            result_dict[smu.get('user_send_id')]['user_name'] = str(user.nickName)
            result_dict[smu.get('user_send_id')]['user_avatar'] = str(user.img_id)
            result_dict[smu.get('user_send_id')]['count'] = smu.get('count', 0)
            result_dict[smu.get('user_send_id')]['data'] = self.get_short_messages_join(sm_list)

            result.append(result_dict)
        return json_response(result)

    def get_short_messages_join(self, sm_list, user_send_id= None):
        result_list = list()
        for sm in sm_list:
            result_dict = dict()
            result_dict.update(sm.__dict__)
            result_dict['short_messages_user_send_id'] = sm.user_send.id
            result_dict['short_messages_user_send_name'] = str(sm.user_send.username)
            result_dict['short_messages_user_send_avatar'] = str(sm.user_send.img_id)
            result_dict['short_messages_user_receive_id'] = sm.user_receive.id
            result_dict['short_messages_user_receive_name'] = str(sm.user_receive.username)
            result_dict['short_messages_user_receive_avatar'] = str(sm.user_receive.img_id)
            result_dict['add_time'] = datetime.strftime(sm.add_time, '%Y-%m-%d %H:%M:%S')
            if str(user_send_id) == str(sm.user_send.id):
                result_dict['is_send'] = 1
            else:
                result_dict['is_send'] = 0

            result_dict.pop('_state')
            result_list.append(result_dict)
        return result_list




class GetShortMessagesList(Resource):
    def get(self, request, *args, **kwargs):
        return self.get_short_messages_list(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.get_short_messages_list(request.POST)

    def get_short_messages_list(self, data):
        user_send_id = data.get('user_send_id', 0)
        user_receive_id = data.get('user_receive_id', 0)
        read_time = data.get('read_time', '')
        page = data.get('page', 1)
        page_size = data.get('page_size', 5)
        if not user_send_id or \
           not user_receive_id or \
           not read_time:
            return params_error()

        sm_list = ShortMessages.objects.filter((Q(user_send_id=user_send_id) & Q(user_receive_id=user_receive_id)) | (Q(user_send_id=user_receive_id) & Q(user_receive_id=user_send_id)),
                                               add_time__lt=read_time).order_by('add_time')
        # page action
        p = Paginator(sm_list, page_size)
        rows = p.page(page)
        result = dict()
        result['page'] = page
        result['data'] = GetUserNewShortMessages().get_short_messages_join(rows,user_send_id)
        return json_response(result)


# 联系人列表
class Linkman(Resource):
    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.linkman(request.POST)

    
    def linkman(self,data):
        user_send_id = data.get('user_send_id', 0)
        sm_list = ShortMessages.objects.filter(user_send_id=user_send_id)    
        result_list = []
        for sm in sm_list:
            result = dict()
            if sm.user_receive_id != sm.user_receive.id:
                return json_response({
                    "msg":"联系人信息不一致，请联系麻酱猫"
                })
            result["user_id"] = sm.user_receive_id
            result["user_image"] = sm.user_receive.images
            result["username"] = sm.user_receive.username
            result["sex"] = sm.user_receive.sex
            result_list.append(result)
        run_function = lambda x, y: x if y in x else x + [y]
        data = reduce(run_function, [[], ] + result_list)
        return json_response({"msg":data})