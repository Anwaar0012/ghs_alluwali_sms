from django.contrib import admin

# Register your models here.
from .models import Employee
# @admin.register(Employee)
class shoolAdmin(admin.ModelAdmin):
    admin.site.site_header = 'School Management System'
    admin.site.register(Employee)
