from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta
from datetime import datetime
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





class Product(models.Model):
    name = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)
    new_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    old_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank= True, null= True)
    stock = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    image_1 = models.ImageField(upload_to='uploads/product/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='uploads/product/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='uploads/product/', blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return self.name
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(models.Avg('rating'))['rating__avg']  
        return None  
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"



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


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)  
    discount_type = models.CharField(
        max_length=10,
        choices=[('percentage', 'Percentage'), ('flat', 'Flat')],
        default='percentage'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)  
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    per_user_limit = models.PositiveIntegerField(null=True, blank=True) 
    is_active = models.BooleanField(default=True)

    @property
    def is_currently_active(self):
        return self.is_active and self.end_date > datetime.now()

    def __str__(self):
        return self.code

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Bank Transfer', 'Direct Bank Transfer'),
        ('PayPal', 'PayPal'),
        ('Razorpay', 'Razorpay'),
    ]
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='COD')
    is_paid = models.BooleanField(default=False)
    
    shipping_address = models.TextField(null=True, blank=True)
    shipping_pincode = models.CharField(max_length=6, null=True, blank=True)
    shipping_phone_number = models.CharField(max_length=15, null=True, blank=True)
    shipping_state = models.CharField(max_length=50, null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    coupon_applied = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    razorpay_order_id  = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id  = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature  = models.CharField(max_length=255, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(random.randint(10000000, 99999999))
        
        super().save(*args, **kwargs)

        if not self.delivery_date and self.order_date:
            self.delivery_date = self.order_date + timedelta(days=7)
            super().save(update_fields=['delivery_date'])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    

    def apply_coupon(self):
        if self.coupon:
            if self.coupon.discount_type == 'percentage':
                self.discount_amount = (self.total_price * self.coupon.discount_value) / 100
            elif self.coupon.discount_type == 'flat':
                self.discount_amount = self.coupon.discount_value

            self.final_price = max(self.total_price - self.discount_amount, Decimal('0.00'))
        else:
            self.discount_amount = Decimal('0.00')
            self.final_price = self.total_price

        self.save(update_fields=['discount_amount', 'final_price'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT)  
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"

    def save(self, *args, **kwargs):
        
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
        


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=Order.PAYMENT_CHOICES)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.amount} {self.payment_method}"



    

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coupon.code} used by {self.user.username}"
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

    def credit(self, amount):
        self.balance += amount
        self.save()

    def debit(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.save()