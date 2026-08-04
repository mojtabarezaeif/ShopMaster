from django import forms


class OrderForm(forms.Form):

    full_name = forms.CharField(
        max_length=100
    )

    email = forms.EmailField()

    address = forms.CharField(
        widget=forms.Textarea
    )
    

class CouponApplyForm(forms.Form):

    code = forms.CharField(
        max_length=30
    )