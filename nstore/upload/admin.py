from django.contrib import admin

# Register your models here.

from ..upload import models
# Register your models here.


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    search_fields = ['original']
    list_display = ("preview",'original')
    pass
