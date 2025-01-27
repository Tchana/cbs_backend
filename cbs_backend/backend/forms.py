from django import forms
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('email',)
    
    def clean(self):
       password = self.cleaned_data["password"]
       password_confirm = self.cleaned_data["password_confirm"]
       
       if password and password !=password_confirm:
           raise forms.ValidationError("Password do not match")
       
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

       