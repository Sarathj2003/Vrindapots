import re
from django import forms
from store.models import Category,Product,Order,Coupon
from django.core.exceptions import ValidationError
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'tag', 'new_price', 'old_price', 'category', 'description', 'stock','image_1', 'image_2', 'image_3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_deleted=False)

    def clean(self):
        cleaned_data = super().clean()
        new_price = cleaned_data.get("new_price")
        old_price = cleaned_data.get("old_price")
        stock = cleaned_data.get("stock")
        if new_price is not None and new_price < 0:
            self.add_error('new_price', ValidationError("New price cannot be negative."))
        if old_price is not None and old_price < 0:
            self.add_error('old_price', ValidationError("Old price cannot be negative."))
        if stock is not None and stock < 0:
            self.add_error('stock', ValidationError("stock cannot be negative."))
        category = cleaned_data.get("category")
        if category and category.is_deleted:
            self.add_error('category', ValidationError("You cannot select an inactive category."))
        return cleaned_data

    
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_status = self.instance.status
        
        self.fields['status'].choices = [
            (key, value) for key, value in self.fields['status'].choices
            if key != current_status
        ]

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value', 'start_date', 'end_date', 'per_user_limit', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(code) < 3 or len(code) > 6:
            raise ValidationError('Coupon code must be between 3 to 6 characters.')
        if not re.match(r'^[a-zA-Z0-9]*$', code):
            raise ValidationError('Coupon code must only contain alphabets and numbers.')
        return code

    def clean_discount_value(self):
        discount_value = self.cleaned_data.get('discount_value')
        if discount_value < 0:
            raise ValidationError('Discount value cannot be negative.')
        discount_type = self.cleaned_data.get('discount_type')
        if discount_type == 'percentage' and (discount_value <= 0 or discount_value > 100):
            raise ValidationError('For percentage discount, value must be between 1 and 100.')
        return discount_value

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < timezone.now():
            raise ValidationError('Start date cannot be in the past.')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date < timezone.now():
            raise ValidationError('End date cannot be in the past.')
        if end_date < self.cleaned_data.get('start_date'):
            raise ValidationError('End date cannot be before the start date.')
        return end_date

    def clean_per_user_limit(self):
        per_user_limit = self.cleaned_data.get('per_user_limit')
        if per_user_limit < 1:
            raise ValidationError('Per user limit must be at least 1.')
        return per_user_limit