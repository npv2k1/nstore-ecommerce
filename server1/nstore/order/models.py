from decimal import Decimal
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.fields import SmallAutoField
from uuid import uuid4
from ..product.models import Product
from ..customer.models import Customer, Address
from django.utils.html import format_html
import datetime

class OrderStatus(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    serial = models.IntegerField()

    @admin.display
    def colored_name(self):
        return format_html(
            '<span style="color: white; background-color: {};padding: 1px">{}</span>',
            self.color,
            self.name,
        )

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    @property
    def paid_total(self):
        return self.amount - self.discount + self.delivery_fee
    STRIPE = 'STRIPE'
    CASH_ON_DELIVERY = 'CASH_ON_DELIVERY'
    PAYMENT_GATEWAY_TYPE = [
        (STRIPE, 'STRIPE'),
        (CASH_ON_DELIVERY, 'CASH_ON_DELIVERY'),
    ]
    tracking_number = models.UUIDField(primary_key=True, default=uuid4)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(
        OrderStatus, on_delete=models.PROTECT, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_gateway = models.CharField(
        max_length=50, choices=PAYMENT_GATEWAY_TYPE, default=STRIPE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    delivery_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=1)
    delivery_time = models.CharField(max_length=255, null=True)

    billing_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name='shipping_address', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracking_number)

    @admin.display(ordering='created_at')
    def created_time(self):
        return self.created_at


class OrderProduct(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='order_product')
    order_quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='products', null=True)
