from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from account.forms import CustomUserCreationForm


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')


def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/add_user.html', {'form': form})
