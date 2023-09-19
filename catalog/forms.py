from django import forms
from .models import Order

class OrderAddOfferForm(forms.Form):
    offer_id = forms.IntegerField()
    quantity = forms.IntegerField()

class OrderUpdateOfferForm(forms.Form):
    order_offer_id = forms.IntegerField()
    quantity = forms.IntegerField()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['receiver', 'phone', 'email', 'comment']

    # You can add custom labels and widgets here if needed
    # receiver = forms.CharField(
    #     label='Receiver Name',
    #     max_length=100
    # )
    # phone = forms.CharField(
    #     label='Phone Number',
    #     max_length=12
    # )
    # comment = forms.CharField(
    #     label='Comment',
    #     max_length=255,
    #     widget=forms.Textarea
    # )
