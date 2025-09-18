from payment.models import Payment
from django import forms


class DeliveryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['delivered']

        