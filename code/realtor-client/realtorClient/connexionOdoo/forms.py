
from django import forms
from .models import connexionInformation

class odooForm(forms.Form):
   username = forms.CharField( max_length=200)
   password = forms.CharField(max_length=200)