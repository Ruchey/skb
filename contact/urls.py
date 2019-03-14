from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact_form'),
    path('sent/', views.ContactSent.as_view(), name='contact_sent'),
]

