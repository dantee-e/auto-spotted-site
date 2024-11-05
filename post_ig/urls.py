from django.urls import path
from . import views

urlpatterns = [
    path('post-photo/', views.post_photo_ig),
    path('post-carousel/', views.post_carousel_ig),
]
