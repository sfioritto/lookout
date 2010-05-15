from django import forms
from django.contrib.auth.models import User
from webapp.account.models import Account


class CreateAccountForm(forms.Form):

    email = forms.EmailField(max_length=75)
    username = forms.CharField(max_length=30)
    password = forms.CharField(label=(u'Password'),
                               widget=forms.PasswordInput(render_value=False)) 
    repassword = forms.CharField(label=(u'Password'),
                               widget=forms.PasswordInput(render_value=False)) 


    def clean_password(self):
        if self.cleaned_data['password'] == self.data['repassword']:
            return self.cleaned_data['password']
        else:
            raise forms.ValidationError("The passwords you entered in don't match.")


    def clean_username(self):

        username = self.cleaned_data['username']

        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError("This username is already taken.")
        except User.DoesNotExist:
            return username

        
    def clean_email(self):

        email = self.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        try:
            account = Account.objects.get(pk=email)
        except Account.DoesNotExist:
            account = None

        if account or user:
            raise forms.ValidationError("An account for this email address has already been created.")
        else:
            return email
