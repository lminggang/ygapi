import random
import datetime as dt

from users.models import *

from django.core.paginator import Paginator

from Api.resources import Resource
from Api.decorators import *


class GenerateRegisterCode(Resource):
    def get(self, request, *args, **kwargs):
        return self.generate_register_code(request.GET)

    def post(self, request, *args, **kwargs):
        return self.generate_register_code(request.POST)

    def generate_register_code(self, data):
        num = data.get('num', 1)
        try:

            if not num.isdigit():
                num = 1
        except Exception as e:
            num = 1
        if not num:
            return params_error()
        else:
            num = int(num)
        result = list()
        querysetlist = list()
        retister_code = RegisterCode.objects.filter(status=False, add_time__lt=(dt.datetime.now() - dt.timedelta(days=2)))
        p = Paginator(retister_code, num)
        code_list = p.page(1)
        code_list = code_list[0: num]
        num = num - len(code_list)
        result = [code.code for code in code_list]
        for i in range(num):
            code = self.generate_verification_code()
            querysetlist.append(RegisterCode(code=code))
            result.append(code)
        RegisterCode.objects.bulk_create(querysetlist)
        return json_response(result)

    def generate_verification_code(self):
        code_list = []
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))

        myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
        verification_code = ''.join(myslice)  # list to string
        return verification_code.upper()
