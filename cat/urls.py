from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^panel/category/list/$', views.cat_list, name = 'cat_list'),
    url(r'^panel/category/add/$', views.cat_add, name = 'cat_add'),
    url(r'^panel/category/del/(?P<pk>\d+)/$',views.cat_delete, name = 'cat_delete'),
   
]