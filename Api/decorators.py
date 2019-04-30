from Api.utils import *

def userinfo_required(func):
    def _wrapper(self,request, *args, **kwarg):
        user=request.user
        if not user.is_authenticated:
            return not_authenticated()
        return func(self,request, *args, **kwarg)
    return _wrapper