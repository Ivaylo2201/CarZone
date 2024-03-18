from django.contrib import admin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'first_name',
        'last_name', 'email',
        'is_staff', 'is_active',
        'location', 'phone_number',
        'last_login', 'date_joined'
    ]

    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    list_filter = ['is_staff', 'is_active', 'location']
    readonly_fields = ['date_joined']
    list_per_page = 20
