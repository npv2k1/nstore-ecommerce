from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import *
from ..core.serializers import UserSerializer, UserUpdateSerializer
from ..core.models import User
from drf_writable_nested.serializers import WritableNestedModelSerializer
from ..upload.serializers import AttachmentSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CustomerAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = CustomerAddress
        fields = '__all__'


class CreateCustomerAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = CustomerAddress
        fields = '__all__'
    def create(self, validated_data):
        user_address = validated_data.pop('address')
        address = Address.objects.create(**user_address)
        customer_address = CustomerAddress.objects.create(
             customer=self.context['customer_id'],address=address,**validated_data)        
        return customer_address



class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    address = CustomerAddressSerializer(many=True, read_only=True)
    avatar = AttachmentSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone',
                  'birth_date', 'membership', 'address', 'phone', 'avatar', 'bio']


class CustomerUpdateSerializer(WritableNestedModelSerializer):
    user = UserUpdateSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'user', 'avatar', 'bio']
