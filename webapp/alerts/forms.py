from django import forms

class CreateAlertForm(forms.Form):

    term = forms.CharField(max_length=256)

class DisableAlertForm(forms.Form):
    
    id = forms.CharField()
