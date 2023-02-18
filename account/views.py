from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from .forms import CustomUserCreationForm, EditUserForm


def user_registration_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    context = {
        "UserRegistrationForm": form
    }
    return render(request, 'account/user_registration.html', context)


@login_required
def user_profile_view(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        print("form", form)
        if form.is_valid():
            user = form.save(commit=False)
            profile_image = form.cleaned_data['profile_image']
            print("profile_image:", profile_image)
            user.profile_image = profile_image
            user.save()
            messages.success(request, 'Your profile has been updated.')
            context = {
                "EditUserDataForm": form
            }
            return redirect('user_profile')
    else:
        form = EditUserForm(instance=request.user)
    context = {
        "EditUserDataForm": form
    }
    return render(request, 'account/user_profile.html', context)


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('user_profile')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully!")
                return redirect('user_profile')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = AuthenticationForm(request)
    conntext = {
        "UserAuthenticationForm": form
    }
    return render(request, 'account/user_login.html', conntext)


def user_logout_view(request):
    logout(request)
    return redirect('user_login')


# change password with old password
def user_change_password_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(request.user, request.POST)
            if fm.is_valid():
                user = fm.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('user_profile')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            fm = PasswordChangeForm(request.user)
        context = {
            "PasswordChangeForm": fm
        }
        return render(request, 'account/user_change_password.html', context)
    else:
        return redirect('user_login')


def user_reset_password_view(request):
    pass


def user_forgotten_password_view(request):
    pass

