# -*- coding: utf-8 -*-

from django.db import models


class Contact(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(max_length=50, blank=True, verbose_name='email')
    body = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return "{} {}".format(self.name, self.phone)



class Files(models.Model):

    file = models.ImageField(upload_to='contact', blank=True, null=True, verbose_name='Файл')
    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.file.name
