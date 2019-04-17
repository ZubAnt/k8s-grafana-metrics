from django.contrib import admin
from django.contrib.admin import ModelAdmin

from da.models import Dashboard


class DashboardAdmin(ModelAdmin):
    pass


admin.site.register(Dashboard, DashboardAdmin)

