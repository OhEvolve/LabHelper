#from django.conf.urls import url
from django.urls import path

from bootcamp.groups import views

urlpatterns = [
    # overview of user current groups
    path('', views.groups, name='groups'),
    # create a new group
    path('create_group/', views.create_group, name='create_group'),
    # join group URLs (TODO)
    path('join_request/',   views.join_request,   name='join_request'),
    # manage group
    path('manage_group/<int:group_id>/',   views.manage_group,   name='manage_group'),
    # leave group (TODO)
    path('leave_group/',   views.leave_group,   name='leave_group'),
    # delete group (TODO)
    path('delete_group/',   views.delete_group,   name='delete_group'),
    # transfer admin permissions
    path('transfer_admin/',   views.transfer_admin,   name='transfer_admin'),
]
