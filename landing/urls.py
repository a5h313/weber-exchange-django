from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('<slug:slug>', views.detail, name='detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback-list/', views.UserFeedbackListView.as_view(), name='feedback-list'),
    path('feedback-detail/<int:pk>', views.UserFeedbackDetailView.as_view(), name='feedback-detail'),
    path("toggle-favorite/<int:post_id>/", views.toggle_favorite, name="toggle-favorite"),
    path('thanks/', views.thanks, name='thanks'),
]
