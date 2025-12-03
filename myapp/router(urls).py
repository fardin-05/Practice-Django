
from django.urls import path,include
from rest_framework.routers import SimpleRouter
from product.views import ProductViewSet, CategoryViewSet
router = SimpleRouter()
router.register('product', ProductViewSet)
router.register('category', CategoryViewSet)



