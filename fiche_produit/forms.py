from django import forms
from django.forms import fields

from .models import Product, ProductCard

class ProductModelForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fld in self.fields:
            self.fields[fld].widget.attrs={
                'class': 'form-control'
            }


class FPModelForm(forms.ModelForm):

    class Meta:
        model = ProductCard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fld in self.fields:
            self.fields[fld].widget.attrs={
                'class': 'form-control'
            }
