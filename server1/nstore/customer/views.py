
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
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import *
from .serializers import *


class CustomerViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post']
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerUpdateSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['POST', 'PUT'], permission_classes=[IsAuthenticated])
    def phone(self, request):
        user = self.request.user
        customer_phone = request.data.get('phone')
        # TODO: verify phone number

        customer_id = Customer.objects.filter(
            user_id=user.id).update(phone=customer_phone)

        return JsonResponse({'phone': customer_phone})


class CustomerAddressViewSet(ModelViewSet):
    queryset = CustomerAddress.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return CustomerAddress.objects.filter(customer=customer_id).all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        serializer = CreateCustomerAddressSerializer(data=request.data, context={
            'customer_id': customer_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerAddressSerializer
        elif self.request.method == 'POST':
            return CreateCustomerAddressSerializer
        return CustomerAddressSerializer
