from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from ..upload.models import Attachment


class Group(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    details = models.TextField(null=True, blank=True)
    image = models.ForeignKey(Attachment, on_delete=models.CASCADE, blank=True, null=True,
                              related_name='category_image')
    icon = models.CharField(max_length=255, null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True, related_name='category')

    def __str__(self):
        return self.name


class Product(models.Model):
    SIMPLE = 'simple'
    VARIABLE = 'variable'
    PRODUCT_TYPE = [
        (SIMPLE, 'Simple'),
        (VARIABLE, 'Variable'),
    ]
    PUBLISH = 'publish'
    DRAFT = 'draft'
    STATUS = [
        (PUBLISH, 'Publish'),
        (DRAFT, 'Draft'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='product_group')
    product_type = models.CharField(
        max_length=50, choices=PRODUCT_TYPE, default=SIMPLE)
    categories = models.ManyToManyField(
        Category, related_name='product_categories')
    description = models.TextField(null=True)
    in_stock = models.BooleanField(default=True)
    gallery = models.ManyToManyField(
        Attachment, blank=True, related_name='product_gallery')
    image = models.ForeignKey(Attachment, on_delete=models.CASCADE,
                              blank=True, null=True, related_name='product_image')
    status = models.CharField(max_length=50, choices=STATUS, default=DRAFT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=255)

    @admin.display
    def preview(self):
        return format_html(
            '<img src="{}"/>',
            self.image.thumbnail,
        )

    def __str__(self):
        return self.name
