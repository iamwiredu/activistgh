from django import forms
from home.models import Product, RelatedImages, Category, Payment,Size39to46, MediumLargeStock
from .models import DeliveryPriceByRegion, DeliveryPriceByAccra

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
        fields = ['medium','large','xl','xl2','xl3']
        labels = {
            'medium': 'Medium',
            'large': 'Large',
            'xl': 'XL',
            'xl2': '2xl',
            'xl3': '3xl',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','image','product_category','description','size_set','price','discount_price']

        labels ={
            'discount_price':'Discount Price',
        }
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



class DeliveryPriceByAccraForm(forms.ModelForm):
    class Meta:
        model = DeliveryPriceByAccra
        fields = [
            'adenta',
            'achimota',
            'circle',
            'lapaz',
            'west_hills',
            'dome',
            'ashaley_botwe',
            'madina',
            'east_legon',
            'west_land',
            'north_legon',
            'legon_campus',
            'dansoman',
            'mataheko',
            'cantonments',
            'labone',
            'osu',
            'spintex',
            'tema',
            'kwabenya',
            'lakeside',
            'ashongman',
            'adjiringanor',
            'east_legon_hills',
            'airport_area',
            'teshie',
            'not_listed',
        ]
        labels = {
            'adenta': 'Adenta',
            'achimota': 'Achimota',
            'circle': 'Circle',
            'lapaz': 'Lapaz',
            'west_hills': 'West Hills',
            'dome': 'Dome',
            'ashaley_botwe': 'Ashaley Botwe',
            'madina': 'Madina',
            'east_legon': 'East Legon',
            'west_land': 'West Land',
            'north_legon': 'North Legon',
            'legon_campus': 'Legon Campus',
            'dansoman': 'Dansoman',
            'mataheko': 'Mataheko',
            'cantonments': 'Cantonments',
            'labone': 'Labone',
            'osu': 'Osu',
            'spintex': 'Spintex',
            'tema': 'Tema',
            'kwabenya': 'Kwabenya',
            'lakeside': 'Lakeside',
            'ashongman': 'Ashongman',
            'adjiringanor': 'Adjiringanor',
            'east_legon_hills': 'East Legon Hills',
            'airport_area': 'Airport Area',
            'teshie': 'Teshie',
            'not_listed':'Not listed',
        }

class DeliveryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['delivered']
