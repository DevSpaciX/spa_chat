from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


from django.urls import reverse
from django.views import View

from .forms import SignUpForm, LoginForm


class HomePageView(View):
    def get(self, request):
        return render(request, "home.html")


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Redirecting")
            return redirect(reverse("room:rooms"))
        return render(request, "signup.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                print("Redirecting")
                return redirect(reverse("room:rooms"))
            form.add_error(None, "Invalid username or password")
        return render(request, "login.html", {"form": form})
