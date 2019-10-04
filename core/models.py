from django.contrib.auth.models import AbstractUser
from photolog.models import Catalog, PhotoObject
from django.utils.html import format_html
from django.conf import settings
from django.urls import reverse
from django.db import models
from photolog import utils
from core import fields

import os
import PIL



STATUS_CHOICES = (
    ('draft', 'Черновик'),
    ('published', 'Опубликовано'),
    )

QUANTITY_DOORS = (
    (2, '2'),
    (3, '3'),
    (4, '4'),
    )




class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')


class PublishedHomePageManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(publish=True)


class User(AbstractUser):

    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    def thumb(self):
        if self.avatar:
            return format_html('<img src="{0}" width="100px"/>', self.avatar.url)
        return 'пусто'

    thumb.short_description = 'Превью'


class DefInfo(models.Model):

    ph = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    soc = models.CharField(max_length=200, verbose_name='Соцсеть')
    email = models.EmailField(max_length=200, verbose_name='Почта')

    class Meta:
        verbose_name = 'Основную информацию'
        verbose_name_plural = 'Основная информация'

    def __str__(self):
        return self.ph


class CommonInfo(models.Model):
    'Абстрактная модель для общих полей'

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.CharField(max_length=160, blank=True, null=True, verbose_name='Краткое описание')
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ключевые слова')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

    class Meta:
        abstract = True


class HomePage(models.Model):
    """Данные для главной страницы"""

    main_content = models.TextField(blank=True, verbose_name='Основной текст')
    send_content = models.TextField(blank=True, verbose_name='Текст для "Напишите нам"')
    catalog = models.ManyToManyField(Catalog, blank=True, verbose_name='Случайные фото из каталогов')
    publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    objects = models.Manager()
    published = PublishedHomePageManager()

    class Meta:
        verbose_name = 'Данные главной страницы'
        verbose_name_plural = 'Данные главной страницы'

    def html_main(self):
        return format_html(self.main_content)

    def html_send(self):
        return format_html(self.send_content)


class Partitions(CommonInfo):

    COVER = 'cover'

    url = models.CharField(max_length=100, db_index=True, verbose_name='URL')
    cover = models.ImageField(upload_to=COVER, blank=True, null=True, verbose_name='Обложка')
    content = models.TextField(blank=True, verbose_name='Содержание')
    template_name = models.CharField(max_length=70, blank=True,
                                    help_text="Пример: 'core/contact_page.html'", verbose_name='Имя шаблона')
    sort = models.SmallIntegerField(default=1, verbose_name='Порядок')
    catalog = models.ManyToManyField(Catalog, blank=True, verbose_name='Каталоги')
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        verbose_name = 'Страницы'
        verbose_name_plural = 'Страницы'
        ordering = ('sort',)

    @property
    def cover_url_jpg(self):
        if self.cover:
            name, ext = os.path.splitext(os.path.basename(self.cover.url))
            dir = os.path.dirname(self.cover.url)
            file = '{0}.{1}'.format(name, 'jpg')
            return os.path.join(dir, 'JPG', file)
        else:
            return ''

    def thumb(self):
        if self.cover:
            return format_html('<img src="{0}"', self.cover.url)
        return 'пусто'

    thumb.short_description = 'Превью оболжки'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Сначала - обычное сохранение
        super(Partitions, self).save(*args, **kwargs)
        
        # Проверяем, указана ли картинка
        if self.cover:
            self.cover.name = utils.to_webp(self.cover.path, self.cover.name)
            filepath = self.cover.path
            new_db_img = utils.get_rename_path(self.cover.name, self.pk)
            new_file_name = utils.get_rename_path(filepath, self.pk)
            # Создадим обложку
            image = PIL.Image.open(filepath)
            image.thumbnail(settings.COVER_IMAGE_SIZE, resample=PIL.Image.LANCZOS)
            image.save(os.path.normpath(new_file_name))
            self.cover.name = new_db_img
            super(Partitions, self).save(*args, **kwargs)
            image.close()
            utils.to_jpg(self.cover.path)
            if filepath != new_file_name:
                os.remove(filepath)

    
class MaterialsType(models.Model):
    """Тип материалов"""

    title = models.CharField('Название', max_length=200)

    class Meta:
        verbose_name = 'Типы материалов'
        verbose_name_plural = 'Тип материалов'

    def __str__(self):
        return self.title


class Materials(models.Model):
    """Материалы для корпуса и вставок"""

    title = models.CharField('Название', max_length=200)
    logo = models.ImageField('Картинка', upload_to='logos', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    mattype = models.ForeignKey(MaterialsType, on_delete=models.CASCADE, verbose_name='Тип материалов')
    catalog = models.ManyToManyField(Catalog, blank=True, verbose_name='Каталоги')
    
    class Meta:
        verbose_name = 'Материалы'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.title

    def thumb(self):
        if self.logo:
            return format_html('<img src="{0}"/>', self.logo.url)
        return 'пусто'
    thumb.short_description = 'Логотип'


class ProductType(models.Model):
    """Типы изделий"""

    slug = models.SlugField(primary_key=True, max_length=200, verbose_name='Заголовок в URL')
    title = models.CharField(max_length=200, verbose_name='Тип изделия')

    class Meta:
        verbose_name = "Тип изделия"
        verbose_name_plural = "Типы изделий"

    def __str__(self):
        return self.title


class StandardModel(models.Model):
    'Базовые модели изделий'
    
    title = models.CharField(max_length=200, verbose_name='Название')
    article = models.CharField(max_length=10, unique=True, verbose_name='Артикул')
    qdoors = models.SmallIntegerField(choices=QUANTITY_DOORS, default=2, verbose_name='Количество дверей')
    prod_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, verbose_name='Тип изделия')
    angular = models.BooleanField(default=False, verbose_name='Угловой')
    shortdesc = models.CharField(max_length=160, blank=True, null=True, verbose_name='Краткое описание')
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ключевые слова')
    description = models.TextField(blank=True, null=True, verbose_name='Описание html')
    price = models.SmallIntegerField(default=0, verbose_name='Цена от')
    height1 = models.SmallIntegerField(default=2200, verbose_name='Высота от')
    height2 = models.SmallIntegerField(default=2400, verbose_name='Высота до')
    width1 = models.SmallIntegerField(default=1200, verbose_name='Ширина от')
    width2 = models.SmallIntegerField(default=2000, verbose_name='Ширина до')
    depth = models.SmallIntegerField(default=600, verbose_name='Глубина')
    phobj = models.ForeignKey(PhotoObject, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Фотообъект')
    materials = models.ManyToManyField(Materials, blank=True, verbose_name='Материалы')

    class Meta:
        verbose_name = 'Базовая модель'
        verbose_name_plural = 'Базовые модели'

    def __str__(self):
        return self.article

    def thumb(self):

        if self.phobj:
            path = self.phobj.get_thumb_url()
            return format_html('<img src="{0}"/>', path)
        return 'пусто'
    thumb.short_description = 'Картинка'

    def get_absolute_url(self):
        return reverse('baseitem', args=[self.prod_type.slug, str(self.pk)])


