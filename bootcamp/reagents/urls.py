
from django.urls import path

from bootcamp.reagents import views

urlpatterns = [
    # overview of user current reagents
    path('', views.reagents, name='reagents'),
    path('create_liquid/', views.create_liquid, name='create_liquid'),
    path('create_solid/', views.create_solid, name='create_solid'),
    path('create_biologic/', views.create_biologic, name='create_biologic'),
    path('create_solution/', views.create_solution, name='create_solution'),
    path('create_cell/', views.create_cell, name='create_cell'),
    ]


