from django.contrib import admin
from .models import TokenInfo, TokeUsage


class TokenInfoAdmin(admin.ModelAdmin):
    list_display = ['token', 'limit_usage', ]
    list_filter = ['token', 'limit_usage', ]
    search_fields = ['token', 'limit_usage', ]


class TokeUsageAdmin(admin.ModelAdmin):
    list_display = ['token_info', 'date', ]
    list_filter = ['token_info', 'date', ]
    search_fields = ['token_info', 'date', ]


admin.site.register(TokenInfo, TokenInfoAdmin)
admin.site.register(TokeUsage, TokeUsageAdmin)
