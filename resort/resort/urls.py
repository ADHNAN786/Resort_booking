"""
URL configuration for resort project.

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
from django.contrib import admin
from django.urls import path
from website.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LoginPage.as_view(),name='login'),
    path('home',HomePage.as_view(),name='home'),
    path('admin',Admin.as_view(),name='admin'),
    path('resort',ResortView.as_view(),name='resort'),
    path('registration',Registration.as_view(),name='reg'),
    path('payment/<int:id>',Payment.as_view(),name='payment'),
    path('sort',filter,name='sort'),
    path('price',filter_2,name='price'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)