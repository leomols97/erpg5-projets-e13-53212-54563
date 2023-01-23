from django import forms

class odooForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(max_length=200, required=True)
