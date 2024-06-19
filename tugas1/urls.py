"""
URL configuration for tugas1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from tugas1.views import (home, detail_artikel, about, contact)
from tugas1.authentikasi import (akun_login, akun_logout, akun_registrasi)

from berita.api import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('dashboard/', include("berita.urls")),
    path('dashboard/', include("pengguna.urls")),
    
    path('detail/<slug:slug>', detail_artikel, name='detail_artikel'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('authentikasi/login', akun_login, name='akun_login'),
    path('authentikasi/logout', akun_logout, name='akun_logout'),
    path('authentikasi/registrasi', akun_registrasi, name='akun_registrasi'),

    #api
    path('api/author/list', api_author_list),
    path('api/author/detail/<int:id_user>', api_author_detail),
    path('api/kategori/add', api_kategori_add),
    path('api/kategori/list', api_kategori_list),
    path('api/kategori/detail/<int:id_kategori>', api_kategori_detail),
    path('api/artikel/add', api_artikel_add),
    path('api/artikel/list', api_artikel_list),
    path('api/artikel/detail/<int:id_artikel>', api_artikel_detail),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)