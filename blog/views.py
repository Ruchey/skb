from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# import pdb


class ListView(generic.ListView):
    
    queryset = Post.published.filter(rubric__status="published")
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5

class DetailView(generic.DetailView):
    queryset = Post.published
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.published.filter(rubric__status="published")
        return context
