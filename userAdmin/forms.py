from django import forms
from home.models import Product, RelatedImages, Category
from .models import DeliveryPriceByRegion


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
    
class DeliveryPriceByRegionForm(forms.ModelForm):
    class Meta:
        model = DeliveryPriceByRegion
        fields = [
            
            'ashanti',
            'greater_accra',
            'volta',
            'western',
            'eastern',
            'northern',
            'upper_east',
            'upper_west',
            'bono',
            'bono_east',
            'ahafo',
            'savannah',
            'western_north',
            'oti',
            'central',
        ]