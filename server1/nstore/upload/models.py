from django.db import models
from django.contrib import admin
from django.utils.html import format_html
# Create your models here.


class Attachment(models.Model):
    thumbnail = models.CharField(max_length=1024, blank=True, null=True)
    original = models.CharField(max_length=1024, blank=True, null=True)

    @admin.display
    def preview(self):
        return format_html(
            '<img src="{}"/>',
            self.thumbnail,
        )

    def __str__(self):
        return self.original
