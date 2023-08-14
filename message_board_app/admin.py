from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from message_board_app.models import User, Category, Message, Response

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Response)
