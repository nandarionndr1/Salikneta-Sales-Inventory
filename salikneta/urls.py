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
    path('editItemPrice/', views.editItemPrice, name='editItemPrice'),
    path('purchaseOrder/', views.purchaseOrder, name='purchaseOrder'),
    path('backload/', views.backload, name='backload'),
    path('transferOrder/', views.transferOrder, name='transferOrder'),
    path('pos/', views.pos, name='pos'),
    path('sales/', views.sales, name='sales'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('sales_report_detail/', views.sales_report_detail, name='sales_report_detail'),

    path('inventory_report/', views.inventory_report, name='inventory_report'),
    path('inventory_report_detail/', views.inventory_report_detail, name='inventory_report_detail'),

    path('check_notifs/', views.check_notif, name='check_notifs'),
    path('open_notifs/', views.open_notif, name='open_notifs'),

    path('get_num_low_items/', views.get_num_lowstock, name='get_num_lowstock'),
    path('ajax/get_invoicelines_by_salesid/<int:idSales>/', views.get_invoice_by_id, name='get_invoicelines_by_salesid'),
    path('ajax/ajaxAddCategory/', views.ajaxAddCategory, name='ajaxAddCategory'),
    path('ajax/ajaxGetUpdatedCategories/', views.ajaxGetUpdatedCategories, name='ajaxGetUpdatedCategories'),
    path('ajax/ajaxAddSupplier/', views.ajaxAddSupplier, name='ajaxAddSupplier'),
    path('ajax/ajaxGetUpdatedSuppliers/', views.ajaxGetUpdatedSuppliers, name='ajaxGetUpdatedSuppliers'),
    path('ajax/ajaxAddItem/', views.ajaxAddItem, name='ajaxAddItem'),
    path('ajax/ajaxGetUpdatedItems/', views.ajaxGetUpdatedItems, name='ajaxGetUpdatedItems'),
    path('ajax/ajaxGetInStock/', views.ajaxGetInStock, name='ajaxGetInStock'),
    path('ajax/ajaxAddPurchaseOrder/', views.ajaxAddPurchaseOrder, name='ajaxAddPurchaseOrder'),
    path('ajax/ajaxAddBackload/', views.ajaxAddBackload, name='ajaxAddBackload'),
    path('ajax/ajaxSaveDelivery/', views.ajaxSaveDelivery, name='ajaxSaveDelivery'),
    path('ajax/ajaxTransferOrder/', views.ajaxTransferOrder, name='ajaxTransferOrder'),
    path('ajax/ajaxInTransitTO/', views.ajaxInTransitTO, name='ajaxInTransitTO'),
    path('ajax/ajaxFinishedTO/', views.ajaxFinishedTO, name='ajaxFinishedTO'),
    path('ajax/ajaxCancelTO/', views.ajaxCancelTO, name='ajaxCancelTO'),

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)