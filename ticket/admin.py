from django.contrib import admin
from .models import Admin, User, ToDo, InProgress,Done
# Register your models here.
admin.site.register(User)
admin.site.register(ToDo)
admin.site.register(InProgress)
admin.site.register(Done)