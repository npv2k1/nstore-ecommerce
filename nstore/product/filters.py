from django_filters.rest_framework import FilterSet
from .models import Product, Category


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'categories__slug': ['exact'],
            'group__slug': ['exact']
        }


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'group__slug': ['exact']
        }
