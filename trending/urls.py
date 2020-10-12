from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^panel/trending/$',views.trending_add, name = 'trending_add'),
    url(r'^panel/trending/list/$',views.trending_list, name = 'trending_list'),
    url(r'^panel/trending/del/(?P<pk>\d+)/$', views.trending_delete, name = 'trending_delete'),
    url(r'^panel/trending/edit/(?P<pk>\d+)/$', views.trending_edit, name = 'trending_edit'),
]