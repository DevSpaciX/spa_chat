from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.contrib import messages
from django.urls import reverse

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect("user:homepage")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def frontpage(request):
    return render(request,"homepage.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("user:homepage"))
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')