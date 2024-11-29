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
from .models import ServiceRequest
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Handle form submission
            service_type = request.POST.get('service_type')
            description = request.POST.get('description')
            uploaded_file = request.FILES.get('file')  # Handle file upload

            try:
                # Create a new service request
                service_request = ServiceRequest.objects.create(
                    user=request.user,
                    service_type=service_type,
                    description=description,
                    file_upload=uploaded_file,  # Match your model's field name
                    status='pending'
                )

                messages.success(request, 'Service request submitted successfully!')
                return redirect('index')  # Redirect to prevent form resubmission

            except Exception as e:
                messages.error(request, f'Error submitting request: {str(e)}')
                return redirect('index')

        # GET request handling
        service_requests = ServiceRequest.objects.filter(user=request.user).order_by('-submitted_at')
        return render(request, 'LoggedIn/main.html', {'service_requests': service_requests})
    else:
        return render(request, "LoggedOut/landing.html")
    
    
def user_login(request):
    if request.user.is_authenticated:
        return render(request, 'LoggedIn/main.html', {})
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            # Authenticate user with email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Redirect to 'index' or 'home' after successful login
                else:
                    messages.error(request, "Invalid password. Please try again.")
            else:
                messages.error(request, "Email does not exist.")
            
            return render(request, "LoggedOut/login.html")
        else:
            return render(request, "LoggedOut/login.html")
     
def user_signup(request):
    if request.user.is_authenticated:
        return render(request, 'LoggedIn/main.html', {})
    else:
        if request.method == 'POST':
            name = request.POST['name']  # Capture the Full Name
            email = request.POST['email']
            password = request.POST['password']


            # Validate email uniqueness
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, "LoggedOut/signup.html")

            # Create user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name  # Save the full name
            user.save()

            # Automatically log in after sign up
            login(request, user)
            return redirect('index')  # Redirect after successful signup
        else:
            return render(request, "LoggedOut/signup.html")


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logging out
