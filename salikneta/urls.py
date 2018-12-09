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
    path('manageCategories/', views.manageCategories, name='manageCategories'),
    path('manageSuppliers/', views.manageSuppliers, name='manageSuppliers'),
    path('manageItems/', views.manageItems, name='manageItems'),
    path('purchaseOrder/', views.purchaseOrder, name='purchaseOrder'),
    path('backload/', views.backload, name='backload'),
    path('pos/', views.pos, name='pos'),
    path('ajax/ajaxAddCategory/', views.ajaxAddCategory, name='ajaxAddCategory'),
    path('ajax/ajaxGetUpdatedCategories/', views.ajaxGetUpdatedCategories, name='ajaxGetUpdatedCategories'),
    path('ajax/ajaxAddSupplier/', views.ajaxAddSupplier, name='ajaxAddSupplier'),
    path('ajax/ajaxGetUpdatedSuppliers/', views.ajaxGetUpdatedSuppliers, name='ajaxGetUpdatedSuppliers'),
    path('ajax/ajaxAddItem/', views.ajaxAddItem, name='ajaxAddItem'),
    path('ajax/ajaxGetUpdatedItems/', views.ajaxGetUpdatedItems, name='ajaxGetUpdatedItems'),
    path('ajax/ajaxGetInStock/', views.ajaxGetInStock, name='ajaxGetInStock'),
    path('ajax/ajaxAddPurchaseOrder/', views.ajaxAddPurchaseOrder, name='ajaxAddPurchaseOrder'),


]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)