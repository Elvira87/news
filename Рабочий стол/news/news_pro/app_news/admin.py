from django.contrib import admin

from .models import Users, News


admin.site.register(Users)
admin.site.register(News)
