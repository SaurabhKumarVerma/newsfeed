from django.conf.urls import url
from .import views

urlpatterns = [
    
    url(r'^panel/subcategory/list/$', views.subcat_list, name = 'subcat_list'),
    url(r'^panel/subcategory/add/$', views.subcat_add, name = 'subcat_add'),
    url(r'^panel/subcategory/del/(?P<pk>\d+)/$',views.subcat_delete, name = 'subcat_delete'),
   
]