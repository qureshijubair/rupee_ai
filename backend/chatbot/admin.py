from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from chatbot.models import UserInfoRecords, UserChatRecords

class UserInfoRecordsAdmin(UserAdmin):
  model = UserInfoRecords
  list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
  list_filter = ['is_active', 'is_staff']
  search_fields = ['username', 'email', 'first_name', 'last_name']
  ordering = ['date_joined']

# Register your models here.
admin.site.register(UserInfoRecords, UserInfoRecordsAdmin)
admin.site.register(UserChatRecords)



