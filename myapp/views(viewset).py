from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Product , Category
from .serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
from rest_framework.mixins import CreateModelMixin , ListModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

#Product Section
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class = ProductSerializer
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock>10:
            return Response({'messege' : "Product With Stock More Then 10 Could Not Be Deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#Category Section
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
            product_count = Count('products')).all()
    serializer_class=CategorySerializer


