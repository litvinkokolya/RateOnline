from django.urls import path
from . import views

urlpatterns = [
    # path('login', views.LoginIn.as_view(), name='index'),
    path('confirmation', views.CheckCode.as_view(), name='confirmation'),
    path('photo_selection', views.PhotoUpload.as_view(), name='photo_selection')
]
