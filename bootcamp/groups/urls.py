from django.conf.urls import url

from bootcamp.groups import views

urlpatterns = [
    # overview of user current groups
    url(r'^$', views.groups, name='groups'),
    # create a new group
    url(r'^create_group/$', views.create_group, name='create_group'),
    # join group URLs (TODO)
    url(r'^join_request/$',   views.join_request,   name='join_request'),
    # manage group
    url(r'^manage_group/$',   views.manage_group,   name='manage_group'),
    # leave group (TODO)
    url(r'^leave_group/$',   views.leave_group,   name='leave_group'),
    # delete group (TODO)
    url(r'^delete_group/$',   views.delete_group,   name='delete_group'),
    # transfer admin permissions
    url(r'^transfer_admin/$',   views.transfer_admin,   name='transfer_admin'),
]
