from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(
        required=False
    )

    phone = forms.CharField(
        required=True
    )
