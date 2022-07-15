from django import forms
from django.forms import fields

from fiche_produit.models import  Order, OrderItem


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fld in self.fields:
            self.fields[fld].widget.attrs={
                'class': 'form-control'
            }
        

class OrderItemModelForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fld in self.fields:
            self.fields[fld].widget.attrs = {
                'class' : 'form-control'
            }