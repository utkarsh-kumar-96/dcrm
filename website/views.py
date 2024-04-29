from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from .forms import SignUpForm, AddRecordForm
from .models import *


# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid Credentials')
            return redirect('home')
    else:
        records = Record.objects.all()
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
    else:
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(pk=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'You are not logged in')
        return redirect('login')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delRec = Record.objects.get(pk=pk)
        delRec.delete()
        messages.success(request, 'Record deleted')
        return redirect('home')
    else:
        messages.success(request, 'You are not logged in')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_rec = form.save()
                messages.success(request, 'Record added')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You are not logged in')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        rec = Record.objects.get(pk=pk)
        form = AddRecordForm(request.POST or None, instance=rec)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You are not logged in')
        return redirect('home')
