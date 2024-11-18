from django.contrib import admin
from .models import Category,Product,Tag,Banner,Review,Coupon,CouponUsage
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Banner)
admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(CouponUsage)

