from datetime import datetime, timedelta

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.contrib import messages
from django.urls import reverse

from spa_chat import settings
from .forms import SignUpForm

def generate_jwt_token(user, jwt=None):
    token_expiry = datetime.now() + timedelta(hours=24) # Установите время жизни токена
    token = jwt.encode({
        'id': user.id,
        'email': user.email,
        'exp': int(token_expiry.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect("room:rooms")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("room:rooms"))
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')