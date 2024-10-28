from django import forms
from store.models import Category,Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'tag', 'new_price', 'old_price', 'category', 'description', 'stock','image_1', 'image_2', 'image_3']


    

