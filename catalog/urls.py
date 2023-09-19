from django.urls import path

from django.urls import path
from .views import (
    CatalogView, CategoryView, ProductRootView, ProductView,
    OrderView, OrderSuccessView, OrderActionsView,
)

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog_root'),
    path('<str:category_alias>/', CategoryView.as_view(), name='catalog_category'),
    path('product/', ProductRootView.as_view(), name='catalog_product_root'),
    path('product/<str:product_alias>/', ProductView.as_view(), name='catalog_product'),
    # path('calculator/', PowerLineSupportView.as_view(), name='catalog_calculator'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
    path('order/<str:cart_action>/', OrderActionsView.as_view(), name='order_actions'),
]
