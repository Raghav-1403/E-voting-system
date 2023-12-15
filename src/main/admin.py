from django.contrib import admin
from .models import votersdb,minerdb,organizations

# Register your models here.
class votersdbamdin(admin.ModelAdmin):
    list_display=('Name','mail','org','pos','votepos',)
admin.site.register(votersdb,votersdbamdin)
class minerdbamdin(admin.ModelAdmin):
    list_display=('Name','mail','org','voteval')
admin.site.register(minerdb,minerdbamdin)
class orgadmin(admin.ModelAdmin):
    list_display=('org',)
admin.site.register(organizations,orgadmin)