from django.contrib import admin
from diabetapp.models import UserInfos,UserDiabeticInfos,UserDailyCalorie


admin.site.register(UserInfos)
admin.site.register(UserDiabeticInfos)
admin.site.register(UserDailyCalorie)
