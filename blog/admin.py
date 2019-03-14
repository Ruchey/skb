from django.contrib import admin
from .models import Post, Rubric, Images



class ImagesInline(admin.TabularInline):
    
    model = Images
    extra = 3
    fields = ('title', 'img', 'thumb')
    readonly_fields = ('thumb',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImagesInline,]
    list_display = ('title', 'slug', 'rubric', 'status', 'publish', 'author')
    list_filter = ('status', 'create_date', 'publish', 'author', 'rubric')
    list_editable = ('status',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    ordering = ('-status',)
