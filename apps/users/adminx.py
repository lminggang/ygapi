import xadmin
from xadmin import views
from .models import WxUsers


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "越光后台管理系统"
    site_footer = "yg"
    # menu_style = "accordion"


class WxUsersAdmin(object):
    list_display = ["token", "nickName", "gender","province","city","country","last_login_time","add_time"]
    list_filter = [ "gender","province","city","country","last_login_time","add_time"]
    search_fields = ["gender","province","city","country" ]

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)