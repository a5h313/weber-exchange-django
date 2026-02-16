from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('<slug:slug>', views.detail, name='detail'),
    path('about/', views.about, name='about'),
]