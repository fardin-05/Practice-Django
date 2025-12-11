#function based view
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Product , Category
from .serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
@api_view(['GET' , 'POST'])
def view_products(request):
    if request.method == 'GET' :
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many = True, )
        return Response(serializer.data)
    if request.method == 'POST' :
       serializer = ProductSerializer(data = request.data)
       serializer.is_valid(raise_exception = True)
       print(serializer.validated_data)
       serializer.save()
       return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def view_specific_products(request , id):
    if request.method == 'GET' :
        product = get_object_or_404(Product , pk = id)
        serializer = ProductSerializer(product  )
        return Response (serializer.data)
    if request.method == 'PUT':
        product = get_object_or_404(Product , pk = id)
        serializer=ProductSerializer(product , data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE' :
        product = get_object_or_404(Product , pk = id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def view_category(request):
    category = Category.objects.annotate(
        product_count = Count('products')).all()
    serializer = CategorySerializer(category, many = True)
    return Response (serializer.data)

@api_view()
def view_specific_category(request , pk):
    category = get_object_or_404 (Category.objects.annotate (product_count = Count('products')) , pk = pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


