# -*- coding: utf-8 -*-
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django import forms

from core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):

    fieldsets = BaseUserAdmin.fieldsets + (
        (u'Дополнительно', {'fields': ('thumb', 'avatar')}),
    )
    readonly_fields = ('thumb', )


@admin.register(models.Partitions)
class PartitionsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Данные', {
            'fields': (('title', 'url'), ('description', 'keywords'), 'status')
            }),
        ('Оформление', {
            'fields': (('thumb', 'cover'),)
            }),
        ('Содержание', {
            'fields': ('content', 'template_name', 'catalog')
            })
        )
    readonly_fields = ('thumb', )
    list_display = ('thumb', 'title', 'url', 'template_name', 'status', 'sort')
    list_filter = ('title', 'status')
    list_editable = ('sort','status',)
    search_fields = ('title', 'content')
    

@admin.register(models.HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'html_main', 'html_send', 'publish')


@admin.register(models.DefInfo)
class DefInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ph', 'soc', 'email')
    list_editable = ('ph', 'soc', 'email')


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.StandardModel)
class StandardModelAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Данные', {
            'fields': (('title', 'article'), ('shortdesc', 'keywords'),
                'description', 'price')
            }),
        ('Конструктив', {
            'fields': (('qdoors', 'prod_type', 'angular'),)
            }),
        ('Размеры', {
            'fields': (('height1', 'height2'),
                       ('width1', 'width2'),
                       'depth', ('thumb', 'phobj'))
            }),
        ('Метериалы', {
            'fields': ('materials',)
            }),
        )
    list_display = ('thumb', 'article', 'title', 'qdoors', 'prod_type', 'angular', 'price')
    search_fields = ('title', 'article', 'qdoors', 'prod_type', 'angular')
    list_filter = ('qdoors', 'prod_type', 'angular')
    list_editable = ('price',)
    readonly_fields = ('thumb', )


@admin.register(models.MaterialsType)
class MaterialsTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Materials)
class MaterialsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Данные', {
            'fields': ('title', 'description', 
                'mattype', 'catalog',
                ('thumb', 'logo'))
            }),
        )
    list_display = ('thumb', 'title', 'mattype')
    readonly_fields = ('thumb', )