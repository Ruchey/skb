from . import models



def partitions(request):

    context = {}
    context['partitions'] = models.Partitions.published.all()

    return context