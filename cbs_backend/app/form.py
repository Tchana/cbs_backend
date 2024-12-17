from django import forms
from django.contrib.auth.models import User


class BookForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    files = forms.FileField()
    category = forms.ChoiceField(choices=(('1', 'bible'),
                                          ('2', 'book'),
                                          ('3', 'biblical_comment'),
                                          ))

class LessonForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    

class RegisterForm(forms.ModelForm):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="pasword")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="confirm_pasword")
    role = forms.ChoiceField(choices=
                             (('1', 'Teacher'),
                              ('2', 'Student'),
                              ))
    class Meta:
        model = User
        fields = [
            'username', 'password', 'password_confirm']        
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm != password_confirm:
            raise forms.ValidationError("Password do not match")
    
        return cleaned_data