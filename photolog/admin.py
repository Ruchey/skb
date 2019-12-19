from django import forms
from django.contrib import admin

from .models import Catalog, PhotoObject, Images


def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = "Опубликовать выбранные объекты"

def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')
make_draft.short_description = "Снять с публикации выбранные объекты"

class ImagesInline(admin.TabularInline):
    
    model = Images
    extra = 3
    fields = ('thumb', 'img', 'sort')
    readonly_fields = ('thumb',)


class PhotoObjectInline(admin.TabularInline):
    
    model = PhotoObject
    extra = 0
    fields = ('thumb', 'title', 'sort', 'status')
    readonly_fields = ('thumb', 'title')


@admin.register(PhotoObject)
class PhotoObjectAdmin(admin.ModelAdmin):

    inlines = [ImagesInline,]
    list_display = ('pk','thumb', 'sort', 'title', 'catalog', 'pub_date', 'status')
    fieldsets = [
        (None, 
            {'fields': (('title', 'keywords', 'shortdesc'), 'description', 'catalog', 'status')}),
    ]
    date_hierarchy = 'pub_date'
    ordering = ('pub_date', 'catalog')
    list_filter = ('pub_date', 'catalog')
    list_display_links = ('thumb',)
    list_editable = ('sort', 'status')
    actions = [make_published, make_draft]


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    inlines = [PhotoObjectInline,]
    list_display = ('title', 'sort', 'status')
    list_editable = ('sort', 'status')
    actions = [make_published, make_draft]

