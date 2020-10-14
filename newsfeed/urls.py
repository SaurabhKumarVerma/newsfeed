from django.contrib import admin
from django.conf.urls import include , url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'', include('main.urls')), 
    url(r'',include('news.urls')),
    url(r'',include('cat.urls')),
    url(r'',include('subcat.urls')),
    url(r'',include('contactform.urls')),
    url(r'',include('trending.urls')),
    url(r'',include('manager.urls')),
    url(r'',include('newsletter.urls')),
    url(r'',include('comment.urls')),
    url(r'',include('blacklist.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
