import json

from django.http.multipartparser import MultiPartParser
from django.middleware.common import MiddlewareMixin
from Api.utils import params_error


class DataConvert(MiddlewareMixin):
    def process_request(self, request):
        method = request.method
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body.decode())
                files = None
            except Exception as e:
                return params_error({
                    'body': '请求数据类型不正确'
                })
                
        elif 'application/x-www-form-urlencoded' in request.content_type:
            data = request.POST
            files = None
        elif 'multipart/form-data' in request.content_type:
            data = request.POST
            # data, files = MultiPartParser(
            #     request.META, request, request.upload_handlers).parse()
        else:
            data = request.GET
            files = None

        if 'HTTP_X_METHOD' in request.META:
            method = request.META['HTTP_X_METHOD'].upper()
            setattr(request, 'method', method)
        setattr(request, method, data)