from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.ChoiceField(widget=forms.PasswordInput, label="pasword")
    password_confirm = forms.ChoiceField(widget=forms.PasswordInput, label="confirm_pasword")
    
    class Meta:
        model = User
        fields = [
            'firstname', 'lastname', 'email', 'password','password_confirm'
        ]
        
    def clean():
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password')
        
        if password and password_confirm != password_confirm:
            raise forms.ValidationError("Password do not match")
    
        return cleaned_data