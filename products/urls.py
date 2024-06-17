"""Main urls."""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from products_app.views import (CategoryViewSet, ProductViewSet, ReviewViewSet,
                                SupplierViewSet)

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('suppliers', SupplierViewSet)
router.register('reviews', ReviewViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
    path('', include('products_app.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', obtain_auth_token, name='api__auth'),
]
