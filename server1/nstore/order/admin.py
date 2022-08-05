from typing import List
from django.contrib import admin
from . import models
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    readonly_fields = ('product_id', 'order_quantity',
                       'unit_price', 'subtotal', 'order')
    can_delete = False
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status', 'payment_gateway']
    search_fields = ['tracking_number', 'customer_id__user__email']
    list_display = ['tracking_number', 'customer_id', 'status', 'created_time',
                    'paid_total', 'payment_gateway', 'billing_address', 'shipping_address']
    readonly_fields = ['tracking_number', 'customer_id',
                       'paid_total', 'payment_gateway', 'billing_address', 'shipping_address', 'amount', 'discount', 'delivery_fee', 'delivery_time', 'created_at', 'updated_at']
    inlines = [OrderProductInline]


@admin.register(models.OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'colored_name', 'serial']
    #
    pass
