from django.contrib import admin
from .models import Message,Pick,Share,Notice,ShortMessages

# Register your models here.
admin.site.register(Message)
admin.site.register(Pick)
admin.site.register(Share)
admin.site.register(Notice)
admin.site.register(ShortMessages)