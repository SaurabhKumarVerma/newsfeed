from django.conf.urls import include , url
from . import views

urlpatterns = [

	url(r'^panel/manager/list/$',views.manager, name = 'manager'),
	url(r'^panel/manager/del/(?P<pk>\d+)/$',views.manager_del, name = 'manager_del'),
	url(r'^panel/manager/group/$',views.manager_group, name = 'manager_group'),
	url(r'^panel/manager/group/add/$',views.manager_group_add, name = 'manager_group_add'),
	url(r'^panel/manager/group/delete/(?P<name>.*)/$',views.manager_group_delete, name = 'manager_group_delete'),
	url(r'^panel/manager/manager/show/(?P<pk>\d+)/$',views.users_groups, name = 'users_groups'),
	url(r'^panel/manager/manager/addtogroup/(?P<pk>\d+)/$',views.users_to_groups, name = 'users_to_groups'),
	url(r'^panel/manager/manager/deltogroup/(?P<pk>\d+)/(?P<name>.*)/$',views.del_users_to_groups, name = 'del_users_to_groups'),
	url(r'^panel/manager/permissions/$',views.manager_perms, name = 'manager_perms'),
	url(r'^panel/manager/permissions/delete/(?P<name>.*)/$',views.manager_perms_del, name = 'manager_perms_del'),
	url(r'^panel/manager/permissions/add/$',views.manager_perms_add, name = 'manager_perms_add'),
	url(r'^panel/manager/permissions/show/(?P<pk>\d+)/$',views.users_perms, name = 'users_perms'),
	url(r'^panel/manager/manager/delperm/(?P<pk>\d+)/(?P<name>.*)/$',views.users_perms_del, name = 'users_perms_del'),
	url(r'^panel/manager/addpermissions/(?P<pk>\d+)/$',views.users_perms_add, name = 'users_perms_add'),
	url(r'^panel/manager/addpermissionstogroup/(?P<name>.*)/$',views.group_perms, name = 'group_perms'),
	url(r'^panel/manager/group/delperm/(?P<gname>.*)/(?P<name>.*)/$',views.group_perms_del, name = 'group_perms_del'),
	url(r'^panel/manager/group/adperm/(?P<name>.*)/$',views.group_perms_add, name = 'group_perms_add'),

   
]