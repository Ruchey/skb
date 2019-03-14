from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:pk>/', views.get_image, name='get_image'),

]

