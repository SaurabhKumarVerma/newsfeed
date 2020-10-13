from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^comment/add/news/(?P<pk>\d+)/$',views.news_cm_add, name = 'news_cm_add'),
    url(r'^panel/comment/list/$',views.comment_list, name = 'comment_list'),
    url(r'^panel/comment/del/(?P<pk>\d+)/$',views.comment_del, name = 'comment_del'),
    url(r'^panel/comment/confirmed/(?P<pk>\d+)/$',views.comment_confirm, name = 'comment_confirm'),
    
   
] 
