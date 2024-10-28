from django import forms
from store.models import Category,Product,ProductImage

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'tag', 'new_price', 'old_price', 'category', 'description', 'stock']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return None  
        return image
    

class ImageCountForm(forms.Form):
    image_count = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(5)],  # Choices from 0 to 4
        label="Number of Images",
        initial=0,
    )