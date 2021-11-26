
from django.conf import settings
from django.contrib import admin

from django.db import models
from ..upload.models import Attachment


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_nstore')
    avatar = models.ForeignKey(
        Attachment, on_delete=models.PROTECT, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

    def __str__(self):
        return self.street_address+', '+self.state+', '+self.city+', '+self.country+', '+self.zip


class CustomerAddress(models.Model):
    BILLING = 'billing'
    SHIPPING = 'shipping'
    ADDRESS_TYPE = [
        (BILLING, 'Billing'),
        (SHIPPING, 'Shipping'),
    ]
    title = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    type = models.CharField(
        max_length=50, choices=ADDRESS_TYPE, default=BILLING)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='address', null=True)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name='address', null=True)

    def __str__(self):
        return self.title
