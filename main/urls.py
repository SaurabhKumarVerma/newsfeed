from django.conf.urls import url
from . import views
from django.conf.urls.static import static

urlpatterns = [
    
    url(r'^$', views.home, name = 'home'), 
    url(r'^about/$', views.about , name = 'about'),
    url(r'^panel/$', views.panel, name = 'panel'),
    url(r'^mylogin/$', views.mylogin, name = 'mylogin'),
    url(r'^mylogout/$',views.mylogout, name = 'mylogout'),
    url(r'^panel/settings/$',views.site_setting, name = 'site_setting'),
    url(r'^panel/about/settings/$',views.about_setting, name = 'about_setting'),
    url(r'^contact/$', views.contact, name = 'contact'),
    url(r'^panel/change/password/$',views.change_pass, name = 'change_pass'),
    url(r'^register/$', views.register, name = 'register'),


] 
