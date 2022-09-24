from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout

# Create your views here.
#registration
def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")

    # if they are not logged in
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST or None)
            #check if the form is valod
            if form.is_valid():
                user = form.save()

                # get the raw_password
                raw_password = form.cleaned_data.get('password1')
                #authenticate the user
                user = authenticate(username=user.username, password=raw_password)

                #login the user
                login(request, user)
                return redirect("main:home")
        else:
            form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

#login
def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            username  = request.POST['username']
            password = request.POST['password']

            print(username,password)

            #check the cridensial
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")
                else:
                    return render(request, 'accounts/login.html', {"error":"your account has been disabled."})
            else:
                return render(request, 'accounts/login.html',{"error": "Invalid Username or Password. Try Again."})
        return render(request, 'accounts/login.html')

#logout user
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        print("logout successful")
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")

