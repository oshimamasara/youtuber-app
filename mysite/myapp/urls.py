from django.urls import path
from . import views

urlpatterns = [
    path('youtuber/', views.youtuber, name='youtuber'),
]