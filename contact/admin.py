from django.contrib import admin
from .models import *


class FilesInline(admin.TabularInline):
    
    model = Files


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    inlines = [FilesInline,]


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    pass