from django.conf.urls import url

from bootcamp.groups import views

urlpatterns = [
    url(r'^$', views.groups, name='groups'),
    url(r'^create_group/$', views.CreateGroup.as_view(), name='create_group'),
    url(r'^join_group/$',   views.join_group,   name='join_group'),
]
