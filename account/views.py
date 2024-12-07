from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

# Create your views here.

def account_login(request):
    # If the user is already authenticated, redirect them to their dashboard
    if request.user.is_authenticated:
        if request.user.user_type == '1':  # Check if admin
            return redirect(reverse("adminDashboard"))
        else:  # Voter
            return redirect(reverse("voterDashboard"))

    context = {}
    
    if request.method == 'POST':
        # Authenticate user using email and password
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user with the custom backend
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            
            # Redirect to the appropriate dashboard based on user type
            if user.user_type == '1':  # Admin
                return redirect(reverse("adminDashboard"))
            else:  # Voter
                return redirect(reverse("voterDashboard"))
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid email or password.")
            return redirect("/")  # Redirect to login page

    return render(request, "voting/login.html", context)

def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            # Save user and associated voter info
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)
            voter.admin = user
            user.save()
            voter.save()

            # Notify user that account creation was successful
            messages.success(request, "Account created successfully. You can log in now!")
            return redirect(reverse('account_login'))
        else:
            # Show error message if the forms are not valid
            messages.error(request, "The provided data failed validation.")
    
    return render(request, "voting/reg.html", context)

def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(request, "You need to be logged in to perform this action.")

    return redirect(reverse("account_login"))
