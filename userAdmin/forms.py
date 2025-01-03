from django import forms
from home.models import Product, RelatedImages, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','image','product_category','price','stock']

class RelatedImagesForm(forms.ModelForm):
    class Meta:
        model = RelatedImages
        fields = ['product','image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']