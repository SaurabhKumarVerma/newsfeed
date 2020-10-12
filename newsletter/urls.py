from django.conf.urls import url
from . import views
from django.conf.urls.static import static

urlpatterns = [
    
    url(r'^newsletter/add/$', views.news_letter, name = 'news_letter'),
    url(r'^panel/newsletter/email/$', views.news_email, name = 'news_email'),
    url(r'^panel/newsletter/phoneno/$', views.news_phone, name = 'news_phone'),
    url(r'^panel/newsletter/del/(?P<pk>\d+)/(?P<num>\d+)/$', views.news_del, name = 'news_del'),

] 
