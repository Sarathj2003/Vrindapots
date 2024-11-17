from django import forms
from store.models import Category,Product,Order
from django.core.exceptions import ValidationError

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
        fields = ['status']  # Include only the status field or others as needed.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_status = self.instance.status
        # Exclude the current status from the choices
        self.fields['status'].choices = [
            (key, value) for key, value in self.fields['status'].choices
            if key != current_status
        ]
