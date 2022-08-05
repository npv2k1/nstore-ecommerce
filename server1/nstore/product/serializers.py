from rest_framework import serializers
from ..product import models
from ..upload.serializers import AttachmentSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        lookup_field = 'slug'
        fields = ['name', 'slug', 'icon']


class CategoryChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'slug', 'icon']


class CategorySerializer(serializers.ModelSerializer):
    # group = GroupSerializer(many=False, read_only=True)
    children = CategoryChildrenSerializer(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'slug', 'children', 'icon']


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'icon', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    categories = SimpleCategorySerializer(many=True, read_only=True)
    group = GroupSerializer(many=False, read_only=True)
    gallery = AttachmentSerializer(many=True, read_only=True)
    image = AttachmentSerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'description', 'slug', 'group', 'product_type',
                  'categories', 'gallery', 'image', 'price', 'quantity', 'unit']
