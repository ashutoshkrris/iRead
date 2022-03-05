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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from authentication.middlewares.auth import auth_middleware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import PostSitemap, CategorySitemap, SeriesSitemap, TagSitemap
from core.views import robots

sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap,
    'series': SeriesSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r"^ckeditor/upload/", csrf_exempt(auth_middleware(views.upload)),
        name="ckeditor_upload"),
    re_path(
        r"^ckeditor/browse/",
        csrf_exempt(never_cache(auth_middleware(views.browse))),
        name="ckeditor_browse",
    ),
    path('accounts/', include('authentication.urls')),
    path('accounts/social/', include('social_django.urls'), name='social'),
    path('', include('core.urls')),
    path('payment/', include('payment.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots, name='robots')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'authentication.views.error_404'
handler500 = 'authentication.views.error_500'
