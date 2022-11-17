from django import forms
from .models import *


class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = "__all__"
