from django.contrib import admin
from .models import VisitorLog

# Register your models here.




@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "country", "city", "ip_address", "page", "is_logged_in", "created_at",)

    list_filter = ("is_logged_in", 'ip_address', "created_at",)

    search_fields = ("username","email", "country", "city",  "ip_address", "page",)

    readonly_fields = ("user", "username", "email", "ip_address", "page", "browser", "user_agent", "is_logged_in", "created_at",)

    ordering = ("-created_at",)
