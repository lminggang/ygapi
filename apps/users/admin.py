from django.contrib import admin
from .models import WxUsers, RegisterCode
# Register your models here.

admin.site.register(WxUsers)
admin.site.register(RegisterCode)