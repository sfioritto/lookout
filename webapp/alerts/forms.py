from django import forms

class CreateAlertForm(forms.Form):

    term = forms.CharField(max_length=256)

