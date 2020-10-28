from django.contrib import messages
from django.contrib.auth import (authenticate, login,
                                 logout)
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("blog")
        messages.add_message(
                request, messages.ERROR, _('Invalid username or password'))
        return render(request, "pages/login.html")
    return render(request, "pages/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")
