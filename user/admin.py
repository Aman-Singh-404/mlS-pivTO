from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.contrib.auth.models import User

class DataField(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Personal info'
    verbose_name_plural = 'Personal info'

class ExtendedUser(UserAdmin):
    inlines = [DataField]

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, ExtendedUser)
