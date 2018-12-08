"""SaliknetaPOSIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('verify/', views.log_in_validate, name='verify'),
    path('register/', views.register, name='register'),
    path('register_validate/', views.register_validate, name='register_validate'),
<<<<<<< HEAD
    path('manageCategories/', views.manageCategories, name='manageCategories'),
    path('manageSuppliers/', views.manageSuppliers, name='manageSuppliers'),
    path('manageItems/', views.manageItems, name='manageItems'),
=======
    path('pos/', views.pos, name='pos'),
>>>>>>> 297e8264ff7eb32362b0218d20d1c7fab56b8cdd
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)