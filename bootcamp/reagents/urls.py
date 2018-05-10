
from django.urls import path

from bootcamp.reagents import views

urlpatterns = [
    # overview of user current reagents
    path('', views.reagents, name='reagents'),
    ]