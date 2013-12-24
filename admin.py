from django.contrib import admin
from myproject.tripwire.models import *

class InmateAdmin(admin.ModelAdmin):
    list_display = ('rest', 'last', 'age', 'crime', 'admissiondate', )
    search_fields = ('rest', 'last', )
    list_filter = ('admissiondate', 'crime',)

class NameAdmin(admin.ModelAdmin):
    list_display = ('first', 'last',)
    search_fields = ('first', 'last',)

admin.site.register(Name, NameAdmin)
admin.site.register(Inmate, InmateAdmin)

