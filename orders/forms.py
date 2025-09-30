from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shipping_full_name', 'shipping_email', 'shipping_phone',
            'shipping_address_line1', 'shipping_address_line2',
            'shipping_city', 'shipping_state', 'shipping_postal_code',
            'shipping_country', 'order_notes', 'payment_method'
        ]
        widgets = {
            'shipping_full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'shipping_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'shipping_address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'shipping_address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2 (Optional)'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'order_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Order notes (optional)'}),
            'payment_method': forms.RadioSelect,  # Use RadioSelect for payment method
        }
        labels = {
            'shipping_full_name': 'Full Name',
            'shipping_email': 'Email Address',
            'shipping_phone': 'Phone Number',
            'shipping_address_line1': 'Address Line 1',
            'shipping_address_line2': 'Address Line 2',
            'shipping_city': 'City',
            'shipping_state': 'State/Province',
            'shipping_postal_code': 'Postal Code',
            'shipping_country': 'Country',
            'order_notes': 'Order Notes',
            'payment_method': 'Payment Method',
        }