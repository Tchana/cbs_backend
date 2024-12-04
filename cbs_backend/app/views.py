from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .form import RegisterForm

# Create your views here.

#this view is will be deleted when all apis endpoint will be created

def home(request):
    return render(request, 'home/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            firstame = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(username=username,
                                            email = email, 
                                            password=password,
                                            fname = firstame,
                                            lname = lastname
                                            )
            
        else:
            form  = RegisterForm()
            return render(request, 'accounts/register.html')
        
        context ={'form' : form}
        
        return render(request, 'accounts/register.html', context)
    
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)

        else:
            error_message = "Invalid credentials"
       
    return render(request, 'accounts/login.html', error_message)
        
        
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
    else:
        return redirect('home')
    
# HOME VIEW
# USING DECORATORS

@login_required
def home_view(request):
    return render(request , 'home/home.html')


#protected view

class ProtectedView(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'register/protected')
            
            
        