import django
from django.conf import settings
from django.contrib import admin
from django.urls import path ,include
from django.urls import re_path
from django.views.static import serve   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('users/',include('users.urls')),
]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]