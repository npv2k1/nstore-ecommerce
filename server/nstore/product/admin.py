from django.contrib import admin
from nstore.product import models
# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # list_select_related = ['parent']
    list_filter = [
         "group",
         "categories",   ]
    search_fields = ['name', 'description']
    list_display = ['preview','name','in_stock','price','quantity']
    pass

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass