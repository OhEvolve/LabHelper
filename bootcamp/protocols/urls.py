
from django.urls import path

from bootcamp.protocols import views

urlpatterns = [
    # overview of user current reagents
    path('', views.protocols, name='protocols'),
    path('create_protocol/', views.create_protocol, name='create_protocol'),
    ]


