from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from ..product.views import ProductViewSet, CategoryViewSet, GroupViewSet, product_detail
from ..customer.views import CustomerViewSet, CustomerAddressViewSet
from ..order.views import OrderViewSet, tracking_number_order
from ..setting.views import settings
from ..core.views import RequestPasswordResetEmail
router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('types', GroupViewSet, basename='types')
router.register('customers', CustomerViewSet, basename='customers')
router.register('orders', OrderViewSet, basename='orders')
router.register('address', CustomerAddressViewSet, basename='address')

# URLConf
urlpatterns = router.urls + [
    path("products/<slug:slug>",
         view=product_detail, name="product-detail"),
    path("orders/tracking-number/<slug:slug>",
         view=tracking_number_order, name="tracking-number"),
    path('settings/', view=settings, name='settings'),
    


]
