from django.contrib import admin
from users.models import User, Membership

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['type', 'valid_from', 'valid_to', 'active']
    list_filter = ()
