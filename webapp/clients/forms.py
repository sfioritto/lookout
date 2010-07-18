from django import forms

class CreateClientForm(forms.Form):

    name = forms.CharField(max_length=256, label=(u"Your client's name."))

class DisableClientForm(forms.Form):
    
    id = forms.CharField()

class UpdateClientForm(forms.Form):
    
    id = forms.CharField()
    name = forms.CharField(max_length=256)


