"""mac URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('', views.home),
    path('contact_us_admin/', views.contactus_admin, name='contact_us_admin'),
    path('admin_site/', views.admin_site, name='admin_site'),
    path('contact_us_admin/<int:id>/', views.contactus_admin_details, name='contact_us_admin_details'),
    path('order_approval/', views.admin_order_approval, name='admin_order_approval'),
    path('set_order_approval/<int:id>/', views.set_order_approval, name='set_order_approval'),
    path('order_cancel/<int:id>/', views.order_cancel, name='order_cancel'),
    path('product_creation/', views.product_creation.as_view(), name='product_creation'),
    path('product_update/<int:pk>/update/', views.ProductUpdate.as_view(), name='product_update'),
    path('product_list/', views.products_list, name='product_list'),
    path('successfully_payment/', views.successfully_payment, name='successfully_payment'),
    path('product_delete/<int:pk>/del/', views.ProductDelete.as_view(), name='product_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
