from django import forms
from .models import UzsakymoReview


class UzsakymoReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymoReview
        fields = ("content", "uzsakymas", "reviewer")
        widgets = {"uzsakymas": forms.HiddenInput(), "reviewer": forms.HiddenInput()}
