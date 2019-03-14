from django.shortcuts import render
from django import http
from .models import *

import pdb # pdb.set_trace()

def get_image(request, pk):
    '''Возвращает url запрошенной картинки'''

    if not request.is_ajax():
        return http.HttpResponseBadRequest(
            ('Direct HTTP request is not allowed'))
    url = Images.objects.get(pk=pk).img.url
    return http.HttpResponse(url)
