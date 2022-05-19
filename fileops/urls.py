from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.upload, name='upload'),
    path('Download', views.upload, name='test'),
    path('About', views.about, name='about'),
    path('Contact', views.contact, name='contact')
]
