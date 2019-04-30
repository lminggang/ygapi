import os
import uuid
import imghdr

from users.models import *
from user_operation.models import *
from wish.models import *

from Api.resources import Resource
from Api.decorators import *

class FilePath:
    URL_BASE = 'http://'
    IMAGE_PATH = 'static/'
# http://10.211.55.6:8000/static/a.jpg
# comment api
class upload_images(Resource):
    @userinfo_required
    def post(self, request, *args, **kwargs):
        print()
        path_base = self.check_path(FilePath.IMAGE_PATH)
        result = list()
        for img in request.FILES.getlist('img'):
            img_path = '{}/{}.{}'.format(path_base, str(uuid.uuid1()), imghdr.what(img))
            # storage image
            with open(img_path, 'wb') as file:
                file.write(img.read())
                result.append(self.img_url_join(request.META['HTTP_HOST'], img_path))

        return json_response(result)

    def check_path(self, directory):
        # check path is exist
        # yes return
        # false create path
        directory = os.path.normpath(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def img_url_join(self, ip, path):
        return '{}{}/{}'.format(FilePath.URL_BASE, ip, path)
