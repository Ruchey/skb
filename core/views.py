from photolog.models import PhotoObject
from django.views import generic, View
from django import http
from . import models

from django.shortcuts import render_to_response
from django.template import RequestContext


class IndexView(generic.ListView):

    queryset = models.Partitions.published.all()
    template_name = 'core/index.html'
    context_object_name = 'partitions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_content'] = models.HomePage.published.first().main_content
        context['send_content'] = models.HomePage.published.first().send_content
        return context


class PartitionsView(generic.base.TemplateView):

    def get_obj(self):
        path = self.request.path
        obj = models.Partitions.objects.get(url = path)
        return obj

    def get_template_names(self):
        template_name = self.get_obj().template_name
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partition'] = self.get_obj()
        return context


class BasicView(PartitionsView):
    '''Вывод базовых модулей'''

    def get_context_data(self, **kwargs):

        filter = self.kwargs.get('prodtype', '')
        bases = models.StandardModel.objects.all().filter(prod_type=filter)
        context = super().get_context_data(**kwargs)
        context['bases'] = bases
        return context



class BasicItemView(generic.DetailView):
    '''Вывод подробностей базового модуля'''
    
    model = models.StandardModel
    template_name = 'core/basic_item.html'
    context_object_name = 'item'

        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter = self.kwargs.get('prodtype', '')
        bases = models.StandardModel.objects.all().filter(prod_type=filter)
        phobj_id = []
        for obj in bases:
            phobj_id.append(obj.pk)

        id = self.kwargs.get('pk')
        context['images'] = models.StandardModel.objects.get(pk=id).phobj.images_set.all()
        context['bases'] = bases
        context['context_list'] = phobj_id
        context['url_type'] = 'noajax'
        context['url_get'] = '/base/{}/'.format(filter)
        context['current_photoobj'] = id
        return context


class WorksView(PartitionsView):
    '''Вывод альбома работ'''

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        obj = self.get_obj()
        catalogs = obj.catalog.all()
        photoobjects = []
        phobj_id = []
        
        for cat in catalogs:
            photoobjects.extend(cat.photoobject_set.all())
        for obj in photoobjects:
            phobj_id.append(obj.pk)

        context['phobj'] = photoobjects
        context['context_list'] = phobj_id
        context['url_type'] = 'ajax'
        context['url_get'] = '/works/'
        context['current_photoobj'] = phobj_id[0]
        return context


# class AJAXPost(View):
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.is_ajax():
    #         return http.HttpResponseBadRequest(
    #             ('Direct HTTP request is not allowed'))
    #     if not request.method == 'POST':
    #         return http.HttpResponseBadRequest(
    #             ('GET requests are not allowed'))
    #     return super().dispatch(request, *args, **kwargs)


class WorksItemView(generic.DetailView):
    '''Формируем окно просмотра картинки
        из каталога с описанием
    '''
    model = PhotoObject
    template_name = 'core/gallery_item_view_ajax.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.is_ajax():
            self.template_name = 'core/gallery_item_view.html'
        
        id = self.kwargs.get('pk')
        context['images'] = PhotoObject.objects.get(pk=id).images_set.all()
        return context


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response