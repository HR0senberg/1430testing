"""
URL configuration for siteman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from http.client import responses
from xml.etree.ElementInclude import include

from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from myteacher import views
from myteacher.views import page_not_found_500, index, teacher_page, responce_error, about, rules
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('sosi/cglen/yeban/nash/admin/get-admin/poshol-nahui/ictory/lets-go-hiking', admin.site.urls),
    path("", index, name = 'main_page'),
    path("about/", about, name = "about"),
    path("rules/", rules, name = "rules"),
    path("<slug:slug>/", teacher_page, name = 'teacher'),
    path("responce_error/", responce_error, name = "error"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
handler500 = page_not_found_500