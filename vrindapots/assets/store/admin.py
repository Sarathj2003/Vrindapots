from django.contrib import admin
from .models import Category,Product,Tag,Banner
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Banner)
