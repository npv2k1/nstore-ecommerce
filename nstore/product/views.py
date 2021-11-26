
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from .pagination import DefaultPagination
from .filters import ProductFilter, CategoryFilter
# Create your views here.


class ProductViewSet(ModelViewSet):
    http_method_names = ['get']
    pagination_class = DefaultPagination
    queryset = Product.objects.select_related(
        'image', 'group').prefetch_related("categories", 'gallery').all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']


class CategoryViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Category.objects.filter(parent=None).select_related(
        "image", 'group').prefetch_related('children').all()
    filterset_class = CategoryFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = CategorySerializer
    search_fields = ['group__slug']


class GroupViewSet(ModelViewSet):
    http_method_names = ['get']
    lookup_field = 'slug'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view()
def product_detail(request, slug):
    http_method_names = ['get', 'post', 'patch', 'delete']
    product = get_object_or_404(Product, slug=slug)
    dt = ProductSerializer(product)

    return Response(dt.data)
