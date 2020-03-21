from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Posts)
admin.site.register(PostInfo)
admin.site.register(Comments)
admin.site.register(PushList)
admin.site.register(Followers)
admin.site.register(Like)
admin.site.register(Profile)