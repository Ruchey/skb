from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('base/<str:prodtype>/', views.BasicView.as_view(), name='base'),
    path('base/<str:prodtype>/<int:pk>/', views.BasicItemView.as_view(), name='baseitem'),
    path('works/', views.WorksView.as_view(), name='works'),
    path('works/<int:pk>/', views.WorksItemView.as_view(), name='worksid'),
]

