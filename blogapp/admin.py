from django.contrib import admin
from .models import Category,Author,Blog
# Register your models here.
admin.site.register([Category,Author,Blog])