from django.db import models
import datetime
# Create your models here.

# Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name







# All the products
class Product(models.Model):
    name = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)
    new_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    old_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank= True, null= True)
    image1 = models.ImageField(upload_to='uploads/product/')
    image2 = models.ImageField(upload_to='uploads/product/')
    image3 = models.ImageField(upload_to='uploads/product/')


    def __str__(self):
        return self.name



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