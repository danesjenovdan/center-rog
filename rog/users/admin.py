from django.contrib import admin
from users.models import User, Membership, ConfirmEmail

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['type', 'valid_from', 'valid_to', 'active']
    list_filter = ()


@admin.register(ConfirmEmail)
class ConfirmEmailAdmin(admin.ModelAdmin):
    pass
