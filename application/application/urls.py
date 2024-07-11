from django.contrib import admin
from django.urls import path, include
from django.conf import settings


handler403 = 'application.views.tr_handler403'
handler404 = 'application.views.tr_handler404'
handler500 = 'application.views.tr_handler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mudl.urls')),
    path('users/', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')),]