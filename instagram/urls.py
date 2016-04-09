# URLconf
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='instagram'),
    url(r'^fotos/', views.instagram, name='instagram_photo'),
]