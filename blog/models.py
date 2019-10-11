from django.utils.html import format_html
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db import models
from photolog import utils
import PIL
import os


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class CommonInfo(models.Model):
    'Абстрактная модель для общих полей'
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.CharField(max_length=160, blank=True, null=True, verbose_name='Краткое описание')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        abstract = True


class Rubric(CommonInfo):

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return self.title


class Post(CommonInfo):
    cover = models.ImageField(upload_to='blog/cover', max_length=200, blank=True, null=True, verbose_name='Обложка')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Рубрика')
    slug = models.CharField(max_length=200, unique=True, verbose_name='url статьи')
    body = models.TextField(blank=True, null=True, verbose_name='Текст')
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ключевые слова')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def get_jpg_url(self):
        return utils.get_jpg_path(self.cover.url)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Сначала - обычное сохранение
        super().save(*args, **kwargs)
        
        # Проверяем, указана ли картинка
        if self.cover:
            
            self.cover.name = utils.to_webp(self.cover.path, self.cover.name)
            filepath = self.cover.path
            new_db_img = utils.get_rename_path(self.cover.name, self.pk)
            new_file_name = utils.get_rename_path(filepath, self.pk)

            image = PIL.Image.open(filepath)
            width, height = image.size
            if (width > 800 or height > 800):
                image.thumbnail((800, 800), resample=PIL.Image.LANCZOS)

            image.save(os.path.normpath(new_file_name))
            self.cover.name = new_db_img
            super().save(*args, **kwargs)
            image.close()
            utils.to_jpg(self.cover.path)
            if filepath != new_file_name:
                os.remove(filepath)


class Images(models.Model):

    SIZE_CHOICES = (
        (180, '180'),
        (300, '300'),
        (600, '600'),
        (800, '800')
        )

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    size = models.SmallIntegerField(choices=SIZE_CHOICES, default='300')
    img = models.ImageField(upload_to='blog', verbose_name='Изображение')
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def get_jpg_url(self):

        return utils.get_jpg_path(self.img.url)

    def thumb(self):
        if self.img:
            return format_html('<img src="{0}" width="160px" height="160px">', self.img.url)
        else:
            return '(ПУСТО)'
    thumb.short_description = 'Картинка'

    def save(self, *args, **kwargs):
        # Сначала - обычное сохранение
        super().save(*args, **kwargs)
        
        # Проверяем, указана ли картинка
        if self.img:
            
            self.img.name = utils.to_webp(self.img.path, self.img.name)
            filepath = self.img.path
            new_db_img = utils.get_rename_path(self.img.name, self.pk)
            new_file_name = utils.get_rename_path(filepath, self.pk)

            image = PIL.Image.open(filepath)
            width, height = image.size
            if (width > self.size or height > self.size):
                image.thumbnail((self.size, self.size), resample=PIL.Image.LANCZOS)

            image.save(os.path.normpath(new_file_name))
            self.img.name = new_db_img
            super(Images, self).save(*args, **kwargs)
            image.close()
            utils.to_jpg(self.img.path)
            if filepath != new_file_name:
                os.remove(filepath)