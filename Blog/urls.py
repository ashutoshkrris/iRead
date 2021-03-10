"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from authentication.middlewares.auth import auth_middleware
from django.views.decorators.cache import never_cache
from django.conf.urls import url
from ckeditor_uploader import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r"^ckeditor/upload/", auth_middleware(views.upload), name="ckeditor_upload"),
    url(
        r"^ckeditor/browse/",
        never_cache(auth_middleware(views.browse)),
        name="ckeditor_browse",
    ),
    path('accounts/',include('authentication.urls')),
    path('',include('core.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'authentication.views.error_404'
handler500 = 'authentication.views.error_500'
