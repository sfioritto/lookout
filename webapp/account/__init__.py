from django.contrib.auth.forms import AuthenticationForm

#Django hack to let us put emails in the username field in the login form
AuthenticationForm.base_fields['username'].max_length = 75 
