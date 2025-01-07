from django import forms
from home.models import Product, RelatedImages, Category, Size39to46, MediumLargeStock
from .models import DeliveryPriceByRegion


class Size39to46Form(forms.ModelForm):  
    class Meta:
        model = Size39to46
        fields = ['size39','size40','size41','size42','size43','size44','size45','size46']
        labels = {
            'size39': '39',
            'size40': '40',
            'size41': '41',
            'size42': '42',
            'size43': '43',
            'size44': '44',
            'size45': '45',
            'size46': '46',
        }
class MediumLargeStockForm(forms.ModelForm):
    class Meta:
        model = MediumLargeStock
        fields = ['Medium','large','xl','xl2','xl3']
        labels = {
            'Medium': 'Medium',
            'large': 'Large',
            'xl': 'XL',
            'xl2': '2xl',
            'xl3': '3xl',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','image','product_category','description','size_set','price']
class ProductStockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock']

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