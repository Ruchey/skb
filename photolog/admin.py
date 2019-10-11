from django.contrib import admin

from .models import Catalog, PhotoObject, Images


class ImagesInline(admin.TabularInline):
    
    model = Images
    extra = 3
    fields = ('thumb', 'img')
    readonly_fields = ('thumb',)


class PhotoObjectInline(admin.TabularInline):
    
    model = PhotoObject
    extra = 0
    fields = ('thumb', 'title')
    readonly_fields = ('thumb', 'title')


@admin.register(PhotoObject)
class PhotoObjectAdmin(admin.ModelAdmin):

    inlines = [ImagesInline,]
    list_display = ('pk','thumb', 'title', 'catalog', 'pub_date')
    fieldsets = [
        (None, 
            {'fields': ('title', 'keywords', 'shortdesc', 'description', 'catalog')}),
    ]
    date_hierarchy = 'pub_date'
    ordering = ('pub_date', 'catalog')
    list_filter = ('pub_date', 'catalog')
    list_display_links = ('thumb',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    inlines = [PhotoObjectInline,]

