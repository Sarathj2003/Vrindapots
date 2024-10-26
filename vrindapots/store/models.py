from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

# Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, default='', blank= True, null= True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Banner(models.Model):
    desc = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/banners/')




# All the products
class Product(models.Model):
    name = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)
    new_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    old_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank= True, null= True)
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.name
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(models.Avg('rating'))['rating__avg']  # Calculate average rating
        return None  # Or return a default value like 0
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"




class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  
    comment = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  

    def __str__(self):
        return f"{self.user.username} - {self.product.name} Review"


# class Order(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     address =
#     phone =
#     date =
#     status =

#     def __str__(self):
#         return self.name