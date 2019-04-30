import json
import datetime as dt
from datetime import datetime

from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q

from users.models import *
from user_operation.models import *
from wish.models import *

from Api.resources import Resource
from Api.decorators import *

class NoticeBase:
    COMMENT = 1
    PICK = 2
    PICK_CONTENT = '赞了我'

# comment api
class add_comment(Resource):
    # @userinfo_required
    # def get(self, request, *args, **kwargs):
    #     return self.add_comment(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.add_comment(request.POST)

    def add_comment(self, data):
        # data = request.GET
        # check params
        wish_id = data.get('wish_id', 0)
        user_send_id = data.get('send_user_id', 0)
        user_receive_id = data.get('receive_user_id', 0)
        parent_id = data.get('parent_id', 0)
        content = data.get('content', '')
        images = data.getlist('images', [])
        if not wish_id or \
           not user_send_id or \
           not user_receive_id or \
           not content or \
           len(content) > 30:
            return params_error()

        # images = json.loads(images)
        # create date
        comment = Message()
        comment.wish_id = wish_id
        comment.user_send_id = user_send_id
        comment.user_receive_id = user_receive_id
        comment.parent_id = parent_id
        comment.content = content
        comment.images = json.dumps(images)
        comment.is_read = False
        comment.add_time = datetime.now()
        comment.save()

        # update wish_comment_num
        try:
            wish = Wish.objects.get(id=wish_id)
        except Exception as e:
            return params_error({'msg': 'wish_id not query data'})
        if wish:
            wish.bb_num = wish.bb_num + 1
            wish.save()

        # add notice
        notice.add_notice(user_send_id=user_send_id,
                          user_receive_id=user_receive_id,
                          wish_id=wish_id,
                          action=NoticeBase.COMMENT,
                          action_id=comment.id,
                          content=comment.content,
                          add_time=comment.add_time)

        return json_response({'comment_id': comment.id,
                              'content': comment.content,
                              'images': json.loads(comment.images),
                              'parent_id': comment.parent_id})



class del_comment(Resource):
    def get(self, request, *args, **kwargs):
        return self.del_comment(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.del_comment(request.POST)

    def del_comment(self, data):
        # data = request.GET
        try:
            comment_id = data.get('comment_id', 0)
        except Exception as e:
            return params_error()
        # check params
        if not comment_id:
            return params_error()
        # check date is exist update or create
        try:
            comment = Message.objects.get(id=comment_id)
        except Exception as e:
            return params_error({'msg': 'comment_id not query data'})
        if not comment:
            return params_error()
        else:
            comment.delete()
            try:
                wish = Wish.objects.get(id=comment.wish_id)
            except Exception as e:
                return params_error({'msg': 'wish_id not query data'})
            if not wish:
                wish.bb_num = wish.bb_num - 1
                wish.save()
        return json_response({'comment_id': comment.id})



class get_comment_list(Resource):
    def get(self, request, *args, **kwargs):
        return self.get_comment_list(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.get_comment_list(request.POST)

    def get_comment_list(self, data):
        # data = request.GET
        wish_id = data.get('wish_id', 0)
        page = data.get('page', 1)
        page_size = data.get('page_size', 5)
        # check params
        if not wish_id:
            return params_error()
        comment = Message.objects.filter(wish_id=wish_id).order_by('-id')
        # page action
        p = Paginator(comment, page_size)
        rows = p.page(page)
        result = dict()
        result['page'] = page
        result['data'] = self.get_comment_list_join(rows)
        return json_response(result)

    def get_comment_list_join(self, comment_rows):
        comment_list = list()
        for comment in comment_rows:
            comment_dict = dict()
            comment_dict.update(comment.__dict__)
            comment_dict['comment_user_send_id'] = comment.user_send.id
            comment_dict['comment_user_send_name'] = str(comment.user_send.nickName)
            comment_dict['comment_user_send_avatar'] = str(comment.user_send.img_id)
            comment_dict['comment_user_receive_id'] = comment.user_receive.id
            comment_dict['comment_user_receive_name'] = str(comment.user_receive.nickName)
            comment_dict['comment_user_receive_avatar'] = str(comment.user_receive.img_id)
            comment_dict['add_time'] = datetime.strftime(comment.add_time, "%Y-%m-%d %H:%M:%S")
            comment_dict['images'] = json.loads(comment.images)
            comment_dict.pop('_state')
            comment_list.append(comment_dict)
        return comment_list


class get_user_comment_list(Resource):
    def get(self, request, *args, **kwargs):
        return self.get_user_comment_list(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.get_user_comment_list(request.POST)

    def get_user_comment_list(self, data):
        # data = request.GET
        user_id = data.get('user_id', 0)
        page = data.get('page', 1)
        page_size = data.get('page_size', 5)
        # check params
        if not user_id:
            return params_error()

        comment = Message.objects.filter(user_send_id=user_id).order_by('-id')
        # page action
        p = Paginator(comment, page_size)
        comment_rows = p.page(page)
        result = dict()
        result['page'] = page
        result['data'] = self.user_comment_list_join(comment_rows)
        # print(result)
        return json_response(result)

    def user_comment_list_join(self, comment_list):
        user_comment_list = list()
        for comment in comment_list:
            user_comment_dict = dict()
            user_comment_dict['wish_id'] = comment.wish.id
            user_comment_dict['comment_id'] = comment.id
            user_comment_dict['wish_content'] = comment.wish.content
            user_comment_dict['comment_content'] = comment.content
            user_comment_dict['comment_images'] = json.loads(comment.images)
            user_comment_dict['wish_add_time'] = datetime.strftime(comment.wish.add_time, "%Y-%m-%d %H:%M:%S")
            user_comment_dict['comment_add_time'] = datetime.strftime(comment.add_time, "%Y-%m-%d %H:%M:%S")
            user_comment_dict['wish_user_id'] = comment.wish.wxuser.id
            user_comment_dict['wish_user_name'] = str(comment.wish.wxuser.nickName)
            user_comment_dict['wish_user_avatar'] = str(comment.wish.wxuser.img_id)
            user_comment_dict['comment_user_send_id'] = comment.user_send.id
            user_comment_dict['comment_user_send_name'] = str(comment.user_send.nickName)
            user_comment_dict['comment_user_send_avatar'] = str(comment.user_send.img_id)
            user_comment_dict['comment_user_receive_id'] = comment.user_receive.id
            user_comment_dict['comment_user_receive_name'] = str(comment.user_receive.nickName)
            user_comment_dict['comment_user_receive_avatar'] = str(comment.user_receive.img_id)

            user_comment_dict.update(comment.wish.__dict__)
            user_comment_dict.pop('_state')
            user_comment_dict.pop('add_time')
            user_comment_dict.pop('id')
            user_comment_dict.pop('content')
            user_comment_list.append(user_comment_dict)

        return user_comment_list


# pick api
class add_pick(Resource):
    def get(self, request, *args, **kwargs):
        return self.add_pick(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.add_pick(request.POST)

    def add_pick(self, data):
        # data = request.GET
        # check params
        user_id = data.get('user_id', 0)
        wish_id = data.get('wish_id', 0)
        if not user_id or not wish_id:
            return params_error()
        # check data is exist update or create
        try:
            pick = Pick.objects.get(user_id=user_id, wish_id=wish_id)
        except Exception as e:
            pick = None
        # wish not exist
        try:
            wish = Wish.objects.get(id=wish_id)
        except Exception as e:
            return params_error({'msg': 'wish_id not query data'})

        if not pick:
            pick = Pick()
            pick.user_id =user_id
            pick.wish_id = wish_id
            pick.add_time = datetime.now()
            pick.save()
            wish.up_num = wish.up_num + 1
            wish.save()
        else:
            if not pick.action:
                pick.action = True
                pick.save()
                wish.up_num = wish.up_num + 1
                wish.save()
            else:
                return json_response({'pick_id': pick.id})

        # add notice
        notice.add_notice(user_send_id=user_id,
                          user_receive_id=wish.wxuser_id,
                          wish_id=wish_id,
                          action=NoticeBase.PICK,
                          action_id=pick.id,
                          content=NoticeBase.PICK_CONTENT,
                          add_time=pick.add_time)

        return json_response({'pick_id': pick.id})

class del_pick(Resource):
    def get(self, request, *args, **kwargs):
        return self.del_pick(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.del_pick(request.POST)

    def del_pick(self, data):
        # data = request.GET
        # check params
        pick_id = data.get('pick_id', 0)
        if not pick_id:
            return params_error()

        # check data is exist update or create
        try:
            pick = Pick.objects.get(id=pick_id)
        except Exception as e:
            pick = None
        # wish not exist
        try:
            wish = Wish.objects.get(id=pick.wish_id)
        except Exception as e:
            return params_error({'msg': 'wish_id not query data'})

        if not pick:
            return params_error()
        else:
            pick.action = False
            pick.save()
            wish.up_num = wish.up_num - 1
            wish.save()
        return json_response({'pick_id': pick.id})

class get_user_pick_list(Resource):
    def get(self, request, *args, **kwargs):
        return self.get_user_pick_list(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.get_user_pick_list(request.POST)

    def get_user_pick_list(self, data):
        # data = request.GET
        # check params
        user_id = data.get('user_id', 0)
        page = data.get('page', 1)
        page_size = data.get('page_size', 5)
        if not user_id:
            return params_error()
        # check data is exist update or return param_err
        pick = Pick.objects.filter(user_id=user_id, action=True).order_by('-id')
        # print(pick)
        p = Paginator(pick, page_size)
        pick_rows = p.page(page)
        result = dict()
        result['page'] = page
        result['data'] = self.get_user_pick_list_join(pick_rows)
        return json_response(result)

    def get_user_pick_list_join(self, pick_list):
        user_pick_list = list()
        # return
        for pick in pick_list:
            user_pick_dict = dict()
            user_pick_dict.update(pick.__dict__)
            user_pick_dict.update(pick.wish.__dict__)
            user_pick_dict.update(pick.user.__dict__)

            user_pick_dict['pick_add_time'] = datetime.strftime(pick.add_time, "%Y-%m-%d %H:%M:%S")
            user_pick_dict['wish_add_time'] = datetime.strftime(pick.wish.add_time, "%Y-%m-%d %H:%M:%S")
            user_pick_dict['user_add_time'] = datetime.strftime(pick.user.add_time, "%Y-%m-%d %H:%M:%S")
            user_pick_dict['last_login_time'] = datetime.strftime(pick.user.last_login_time, "%Y-%m-%d %H:%M:%S")
            user_pick_dict['pick_id'] = pick.id


            user_pick_dict.pop('_state')
            user_pick_dict.pop('id')
            user_pick_dict.pop('add_time')
            user_pick_list.append(user_pick_dict)
        return user_pick_list



# share api
class add_share(Resource):
    def get(self, request, *args, **kwargs):
        return self.add_share(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.add_share(request.POST)

    def add_share(self, data):
        # data = request.GET
        # check params
        user_id = data.get('user_id', 0)
        wish_id = data.get('wish_id', 0)
        if not user_id or not wish_id:
            return params_error()
        # create date
        share = Share()
        share.user_id = user_id
        share.wish_id = wish_id
        share.add_time = datetime.now()
        share.save()

        # update share num
        try:
            wish = Wish.objects.get(id=wish_id)
        except Exception as e:
            return params_error({'msg': 'wish_id not query data'})
        if not wish:
            wish.share_num = wish.share_num + 1
            wish.save()
        return json_response({'share_id': share.id})


# notice api
class notice(Resource):
    def get(self, request, *args, **kwargs):
        return self.get_user_notice_list(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.get_user_notice_list(request.POST)

    # add notice
    @classmethod
    def add_notice(self, user_send_id, user_receive_id, wish_id, action, action_id, content, add_time):
        # checkout params
        if not user_send_id or \
           not user_receive_id or \
           not action_id or \
           not action:
            return False

        notice = Notice()
        notice.user_send_id = user_send_id
        notice.user_receive_id = user_receive_id
        notice.wish_id = wish_id
        notice.action = action
        notice.action_id = action_id
        notice.content = content
        notice.add_time = add_time
        notice.save()

        try:
            UserNotice.objects.get(user_id=user_receive_id)
        except Exception as e:
            user_notice = UserNotice()
            user_notice.user_id = user_receive_id
            user_notice.last_read_time = datetime.now() - dt.timedelta(days=1000)
            user_notice.save()
        return True


    # get user notice list
    def get_user_notice_list(self, data):
        # check params
        user_id = data.get('user_id', 0)
        page = data.get('page', 1)
        page_size = data.get('page_size', 5)
        if not user_id:
            return params_error()

        try:
            user_notice = UserNotice.objects.get(user_id=user_id)
            user_notice.last_read_time = datetime.now()
            user_notice.save()
        except Exception as e:
            user_notice = UserNotice()
            user_notice.user_id = user_id
            user_notice.last_read_time = datetime.now()
            user_notice.save()

        notice = Notice.objects.filter(user_receive_id=user_id).order_by('-id')
        # page action
        p = Paginator(notice, page_size)
        rows = p.page(page)
        result = dict()
        result['page'] = page
        result['data'] = self.get_user_notice_list_join(rows)

        return json_response(result)

    def get_user_notice_list_join(self, notices):
        notice_list = list()
        for notice in notices:
            notice_dict = dict()
            notice_dict['user_send_id'] = notice.user_send.id
            notice_dict['user_send_name'] = str(notice.user_send.nickName)
            notice_dict['user_send_avatar'] = str(notice.user_send.img_id)
            notice_dict['notice_content'] = notice.content
            notice_dict['wish_content'] = notice.wish.content
            notice_dict['notice_add_time'] = datetime.strftime(notice.add_time, "%Y-%m-%d %H:%M:%S")
            notice_dict['wish_add_time'] = datetime.strftime(notice.wish.add_time, "%Y-%m-%d %H:%M:%S")

            notice_dict.update(notice.__dict__)
            notice_dict.update(notice.wish.__dict__)

            notice_dict.pop('_state')
            notice_dict.pop('add_time')

            notice_list.append(notice_dict)
        return notice_list

class get_new_notice_count(Resource):
    def get(self, request, *args, **kwargs):
        return self.new_notice_count(request.GET)

    @userinfo_required
    def post(self, request, *args, **kwargs):
        return self.new_notice_count(request.POST)

    def new_notice_count(self, data):
        # check params
        user_id = data.get('user_id', 0)
        if not user_id:
            return params_error()

        try:
            user_notice = UserNotice.objects.get(user_id=user_id)
        except Exception as e:
            user_notice = UserNotice()
            user_notice.user_id = user_id
            user_notice.last_read_time = datetime.now()
            user_notice.save()

        notice = Notice.objects.filter(user_receive_id=user_id, add_time__gt=user_notice.last_read_time)

        return json_response({'count': len(notice)})



