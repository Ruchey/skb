from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.ListView.as_view(), name='posts_list'),
    path('<slug:slug>/', views.DetailView.as_view(), name='post_detail'),
]