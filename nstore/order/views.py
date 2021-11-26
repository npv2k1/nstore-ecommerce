
from pprint import pprint

from django.db.models.aggregates import Count
from django.db.models.query import prefetch_related_objects
# Create your views here.
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import (AllowAny, DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly,
                                        IsAdminUser, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import *
from .pagination import DefaultPagination
from .serializers import *


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post']
    pagination_class = DefaultPagination
    select_related_fields = ['status', 'customer_id']
    prefetch_related_objects = [
        'products__product_id', 'products__product_id__image']

    def create(self, request, *args, **kwargs):

        user = self.request.user
        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)

        serializer = CreateOrderSerializer(data=request.data, context={
                                           'customer_id': customer_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderTrackingSerializer
        elif self.request.method == 'POST':
            return OrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id).select_related(*self.select_related_fields).prefetch_related(*self.prefetch_related_objects).all().order_by('-created_at')


@api_view()
def tracking_number_order(request, slug):
    http_method_names = ['get', 'post', 'patch', 'delete']

    # pprint('dmmmnweiywgurf')
    order = get_object_or_404(Order, tracking_number=slug)

    dt = OrderTrackingSerializer(order)

    return Response(dt.data)
