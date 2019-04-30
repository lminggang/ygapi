from django.contrib import admin

# Register your models here.
from .models import Wish, News,TodayTitle

admin.site.register(Wish)
admin.site.register(News)
admin.site.register(TodayTitle)