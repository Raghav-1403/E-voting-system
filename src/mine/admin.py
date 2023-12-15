from django.contrib import admin
from .models import count,track

# Register your models here.
class countadmin(admin.ModelAdmin):
    list_display=('cou',)
admin.site.register(count,countadmin)
class trackeradmin(admin.ModelAdmin):
    list_display=('trace',)
admin.site.register(track,trackeradmin)