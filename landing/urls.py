from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('<slug:slug>', views.detail, name='detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('thanks/', views.thanks, name='thanks'),
]