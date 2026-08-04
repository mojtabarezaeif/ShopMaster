from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=[
            (1, "⭐"),
            (2, "⭐⭐"),
            (3, "⭐⭐⭐"),
            (4, "⭐⭐⭐⭐"),
            (5, "⭐⭐⭐⭐⭐"),
        ],
        widget=forms.RadioSelect
    )


    class Meta:

        model = Review

        fields = [
            "rating",
            "comment",
        ]