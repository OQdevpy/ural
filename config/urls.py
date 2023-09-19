"""
URL configuration for config project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from avtostan.views import  CertificatesView, FeedbackView
from catalog.views import CatalogView, CategoryView, OrderView, OrderSuccessView, OrderActionsView, ProductRootView, ProductView
from common.views import HomePageView, PageView, country

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),

    path('order/', OrderView.as_view(), name='order'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
    path('order/<str:cart_action>/',
         OrderActionsView.as_view(), name='order_actions'),
    path('<str:country>/', HomePageView.as_view(), name='homepage'),

    path('<str:country>/certs/', CertificatesView.as_view(), name='certs_actions'),
    path('<str:country>/feedback/', FeedbackView.as_view()),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('<str:country>/catalog/', CatalogView.as_view(), name='catalog_root'),
    path('<str:country>/catalog/<str:category_alias>/',
         CategoryView.as_view(), name='catalog_category'),
    path('<str:country>/product/', ProductRootView.as_view(), name='catalog_product_root'),
    path('<str:country>/product/<str:product_alias>/',
         ProductView.as_view(), name='catalog_product'),

    path('<str:country>/<str:page_alias>/', PageView.as_view(), name='page'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
