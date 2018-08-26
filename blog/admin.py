from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Config)
admin.site.register(models.User)
admin.site.register(models.Cate)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.FriendsLink)
admin.site.register(models.Photos)
