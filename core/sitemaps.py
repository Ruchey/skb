from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from core.models import StandardModel, Partitions
from photolog.models import PhotoObject



class IndexSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['index']

    def location(self, item):
        return reverse('index')


class PostSitemap(Sitemap):
    '''Карта сайта по блогам'''

    protocol = 'https'
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.publish



class StandardModelSitemap(Sitemap):
    '''Карта сайта по базовым моделям'''

    protocol = 'https'
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return StandardModel.objects.all()



class WorksSitemap(Sitemap):
    '''Карта сайта для раздела наших работ'''

    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['works']

    def location(self, item):
        return reverse(item)



class WorksIDSitemap(Sitemap):
    '''Карта сайта всех наших работ'''

    protocol = 'https'
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        part = Partitions.objects.get(url = reverse('works'))
        catalogs = part.catalog.all()
        cat_id = []
        for cat in catalogs:
            cat_id.append(cat.pk)
        objs = PhotoObject.objects.filter(catalog__in=cat_id)

        return objs

    def location(self, item):
        return '{0}{1}'.format(reverse('works'), item.pk)