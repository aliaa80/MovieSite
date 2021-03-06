from django.shortcuts import render, redirect
from .models import Account
from .forms import AccountForm
from django.contrib import messages


# Create your views here.
def home(request):
    request.session.load()
    if 'name' in request.session and request.session['name'] is not None:
        return render(request, 'index.html', {'name': request.session['name']})
    else:
        return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        name = request.POST['username']
        pass1 = request.POST['password']
        check = False
        for account in Account.objects.all():
            if account.username == name and account.password == pass1:
                messages.success(request, 'You signed in successfully')
                check = True
                request.session.modified = True
                request.session['name'] = name
                request.session.save()
                return redirect('home')
        if not check:
            messages.success(request, 'Incorrect username or password.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.modified = True
    request.session['name'] = None
    request.session.save()
    return redirect('home')


def signup(request):
    if request.method == "POST":
        form = AccountForm(request.POST or None)
        if form.is_valid():
            pass1 = request.POST['password']
            pass2 = request.POST['confirm-password']
            if pass1 == pass2:
                form.save()
                messages.success(request, 'You signed up successfully')
                return redirect('login')
            else:
                messages.success(request, 'Passwords does\'nt match')
                return render(request, 'signup.html')

    else:
        return render(request, 'signup.html')
