from django.contrib import admin

# Register your models here.
from .models import hashvalue,partymembers,position,partyselection
class posadmin(admin.ModelAdmin):
    list_display=('participant','org',)
admin.site.register(position,posadmin)
class hashadmin(admin.ModelAdmin):
    list_display=('hash_values',)
admin.site.register(hashvalue,hashadmin)
class partadmin(admin.ModelAdmin):
    list_display=('party','party_display','party_pos',)
admin.site.register(partymembers,partadmin)
class selectadmib(admin.ModelAdmin):
    list_display=('pos',)
admin.site.register(partyselection,selectadmib)
