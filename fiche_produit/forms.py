from django import forms

from .models import Product

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
        
    