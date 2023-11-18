from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'bio',
        'username',
        'email',
        'role',
        'confirmation_code',
    )
    list_filter = ('username',)
    search_fields = ('username',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
