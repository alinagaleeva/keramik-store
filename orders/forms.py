from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Last Name'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Country'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'City'}))
    postal_code = forms.CharField(widget=forms.NumberInput(
        attrs={
            'class': 'login__input',
            'placeholder': 'Postal Code'
        }
    ))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Address'}))
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class': 'login__input', 'placeholder': 'Phone'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'country', 'city', 'postal_code', 'address', 'phone')
