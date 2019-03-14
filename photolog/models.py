from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.html import format_html
from django.core import validators
from django.conf import settings
from django.urls import reverse
from django.db import models
from photolog import utils
import os
import PIL



class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Catalog(models.Model):

    title = models.CharField('Название', max_length=200)
    
    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
        
    def __str__(self):
        return self.title


class PhotoObject(models.Model):
    'Фотообъект - объект, у которого больше одной фотографии'

    catalog = models.ForeignKey(Catalog, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=512, blank=True, null=True, verbose_name='Описание')
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ключевые слова')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Фотообъект'
        verbose_name_plural = 'Фотообъекты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_image', args=[self.pk])

    def get_thumb_url(self):

        obj = Images.objects.filter(phobj_id=self.pk)
        if obj.exists():
            return utils.get_prefix_path(obj.first().img.url)
        else:
            return None

    def get_middle_thumb_url(self):

        obj = Images.objects.filter(phobj_id=self.pk)
        if obj.exists():
            return utils.get_prefix_path(obj.first().img.url, 'mid')
        else:
            return None

    def thumb(self):
        path = self.get_thumb_url()
        if path:
            return format_html('<img src="{0}">', path)
        else:
            return '(ПУСТО)'
    thumb.short_description = 'Картинка'


class Images(models.Model):

    img = models.ImageField(upload_to='photolog', verbose_name='Изображение')
    phobj = models.ForeignKey(PhotoObject, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def get_thumb_url(self):
        return utils.get_prefix_path(self.img.url)

    def get_middle_thumb_url(self):
        return utils.get_prefix_path(self.img.url, 'mid')
        
    def thumb(self):
        if self.img:
            path = self.get_thumb_url()
            return format_html('<img src="{0}">', path)
        else:
            return '(ПУСТО)'
    thumb.short_description = 'Картинка'

    def save(self, *args, **kwargs):
        # Сначала - обычное сохранение
        super(Images, self).save(*args, **kwargs)
        
        # Проверяем, указана ли картинка
        if self.img:
            
            self.img.name = utils.to_webp(self.img.path, self.img.name)
            filepath = self.img.path
            new_db_img = utils.get_rename_path(self.img.name, self.pk)
            new_file_name = utils.get_rename_path(filepath, self.pk)
            thumb_file_name = utils.get_prefix_path(new_file_name)
            middle_file_name = utils.get_prefix_path(new_file_name, 'mid')
            # Создадим превьюшку
            image = PIL.Image.open(filepath)
            image = utils.get_box_thumb(image, settings.THUMB_IMAGE_SIZE)
            image.save(os.path.normpath(thumb_file_name))
            # Создадим обложку
            image = PIL.Image.open(filepath)
            image.thumbnail(settings.MIDDLE_SIZE_IMAGE, resample=PIL.Image.LANCZOS)
            image.save(os.path.normpath(middle_file_name))
            # Просто уменьшим картинку до заданного MAX_SIZE_IMAGE
            image = PIL.Image.open(filepath)
            width, height = image.size
            if (width > settings.MAX_SIZE_IMAGE[0]) or (height > settings.MAX_SIZE_IMAGE[1]):
                image.thumbnail(settings.MAX_SIZE_IMAGE, resample=PIL.Image.LANCZOS)
            # Наложение водяного знака
            image = utils.add_watermark(image)
            image.save(os.path.normpath(new_file_name))
            self.img.name = new_db_img
            super(Images, self).save(*args, **kwargs)
            
            image.close()
            if filepath != new_file_name:
                os.remove(filepath)


@receiver(pre_delete, sender=Images)
def img_delete(sender, instance, **kwargs):

    if instance.img.name:
        thumb = instance.get_thumb_url()
        thumb_path = os.path.join(settings.MEDIA_ROOT, os.path.relpath(thumb, settings.MEDIA_URL))

        if os.path.exists(thumb_path):
            os.remove(thumb_path)

        middle = instance.get_middle_thumb_url()
        middle_path = os.path.join(settings.MEDIA_ROOT, os.path.relpath(thumb, settings.MEDIA_URL))

        if os.path.exists(middle_path):
            os.remove(middle_path)

        instance.img.delete(False)
