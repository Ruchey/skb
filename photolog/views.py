from django.shortcuts import render
from django import http
from .models import *


def get_image(request, pk):
    '''Возвращает url запрошенной картинки'''

    if not request.is_ajax():
        return http.HttpResponseBadRequest(
            ('Direct HTTP request is not allowed'))
    webp = Images.objects.get(pk=pk).img.url
    jpg = Images.objects.get(pk=pk).get_jpg_url()
    return http.JsonResponse({'webp': webp, 'jpg': jpg}, status=200)
