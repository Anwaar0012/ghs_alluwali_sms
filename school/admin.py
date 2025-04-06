# school/admin.py
from django.contrib import admin
from .models import SchoolInfo, Slider,AboutUs,CallbackRequest

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'address', 'email', 'phone')
    
admin.site.register(AboutUs)
admin.site.register(CallbackRequest)

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
