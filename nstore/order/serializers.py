
from rest_framework import serializers
from .models import *


from ..upload.serializers import AttachmentSerializer
from ..customer.serializers import AddressSerializer


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class SimpleProductSerializer(serializers.ModelSerializer):
    image = AttachmentSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image',
                  'slug', 'price', 'quantity', 'unit']


class OrderTrackingProductSerializer(serializers.ModelSerializer):
    product_id = SimpleProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderTrackingSerializer(serializers.ModelSerializer):
    products = OrderTrackingProductSerializer(many=True)
    status = OrderStatusSerializer()
    billing_address = AddressSerializer()
    shipping_address = AddressSerializer()
    paid_total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        # fields = ['id','tracking_number','customer_id','status','delivery_fee','delivery_time','products','paid_total','billing_address','shipping_address']
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    # product_id = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    billing_address = AddressSerializer(many=False)
    shipping_address = AddressSerializer(many=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for order_product in order_products:
            OrderProduct.objects.create(order=order, **order_product)
        return order


class CreateOrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_products = validated_data.pop('products')

        order = Order.objects.create(
            **validated_data, customer_id=self.context['customer_id'])
        for order_product in order_products:
            OrderProduct.objects.create(order=order, **order_product)
        return order
