from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^panel/blacklist/list/$', views.black_list, name = 'black_list'),
    url(r'^panel/blacklist/list/add/$', views.ip_add, name = 'ip_add'),
    url(r'^panel/blacklist/ip/del/(?P<pk>\d+)/$',views.ip_del, name = 'ip_del'),
   
]