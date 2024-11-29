from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect 

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'LoggedIn/main.html', {})
    else:
        return render(request, "LoggedOut/landing.html", {})
    

def user_login(request):
    if request.user.is_authenticated:
        return render(request, 'LoggedIn/main.html', {})
    else:
        if request.method == 'POST':
            # Get username and password from POST data
            username = request.POST['username']
            password = request.POST['password']
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to 'index' view after successful login
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, "LoggedOut/login.html")
        else:
            return render(request, "LoggedOut/login.html")
     
def user_signup(request):
    if request.user.is_authenticated:
        return render(request, 'LoggedIn/main.html', {})
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()  # Create the user
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                
                # Automatically log in the new user
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Redirect to 'index' view after successful signup
            else:
                messages.error(request, "Error during signup. Please check your form.")
                return render(request, "LoggedOut/signup.html", {'form': form})
        else:
            form = UserCreationForm()
            return render(request, "LoggedOut/signup.html", {'form': form})