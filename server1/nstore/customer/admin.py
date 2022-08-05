from django.contrib import admin
from . import models


class CustomerAddressInline(admin.TabularInline):
    # autocomplete_fields = ['user']
    min_num = 1
    max_num = 10
    model = models.CustomerAddress
    extra = 0


@admin.register(models.CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['customer','title', 'type', 'address']
    pass


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [CustomerAddressInline]
    list_display = ('user', 'first_name', 'last_name', 'membership', 'phone')
    pass
