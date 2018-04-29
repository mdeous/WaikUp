from django import forms

from .models import Link


class NewLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url', 'title', 'description', 'category']
