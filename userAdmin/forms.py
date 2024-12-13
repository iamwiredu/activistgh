from django import forms
from home.models import Product, RelatedImages


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','image','category','color_tag','description','price','stock']

class RelatedImagesForm(forms.ModelForm):
    class Meta:
        model = RelatedImages
        fields = ['product','image']