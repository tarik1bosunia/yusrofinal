from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import reverse_lazy

# redirect next page
# from requests import utils
from urllib.parse import urlparse, parse_qs

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from account.utils import Util

from .forms import CustomUserCreationForm, EditUserForm, UserLoginForm
from account.models import CustomUser

from cart.models import Cart, CartItem
from cart.views import _cart_id


def user_registration_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # USER ACTIVATION
            email = form.cleaned_data['email']
            current_site = get_current_site(request)
            message = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            data = {
                'subject': "Please activate your account.",
                'body': message,
                'to_email': email
            }

            Util.send_email(data)
            url = reverse('user_login') + f'?command=verification&email={email}'
            # messages.success(request, 'Thank you for registering with us! We are sent a email to your email address. Please verify your email.')
            return redirect(url)

    else:
        form = CustomUserCreationForm()
    context = {
        "UserRegistrationForm": form
    }
    return render(request, 'account/user_registration.html', context)


@login_required(login_url='user_login')
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


@login_required(login_url='user_login')
def user_settings_and_privacy_view(request):
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
    return render(request, 'account/settings_and_privacy.html', context)

def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('user_profile')

    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

                    ex_cart_items = CartItem.objects.filter(user=user)

                    for cart_item in cart_items:
                        if cart_item.product in [ex_item.product for ex_item in ex_cart_items]:
                            # If the item already exists in the user's cart, increase the quantity
                            ex_cart_item = ex_cart_items.get(product=cart_item.product)
                            ex_cart_item.quantity += cart_item.quantity
                            ex_cart_item.save()
                            cart_item.delete()
                        else:
                            # Otherwise, assign the cart item to the user
                            cart_item.user = user
                            cart_item.save()

                except Cart.DoesNotExist:
                    pass
                login(request, user)
                messages.success(request, "Login successfully!")

                referer_url = request.META.get("HTTP_REFERER")
                try:
                    query = urlparse(referer_url).query
                    next_param = parse_qs(query).get('next', [None])[0]
                    print("next param: ", next_param)
                    if next_param:
                        redirect_url = next_param
                    else:
                        redirect_url = reverse('user_profile')
                except Exception as e:
                    print("Warning: Error occurred while parsing referer URL -", e)
                    redirect_url = reverse('user_profile')
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = UserLoginForm(request)
    conntext = {
        "UserAuthenticationForm": form
    }
    return render(request, 'account/user_login.html', conntext)


@login_required(login_url='user_login')
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


def user_activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=uid)
    except (DjangoUnicodeDecodeError, TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations !your email is verified successfully!Now you can login your account")
        return redirect('user_login')
    else:
        messages.error(request, "Invalid Activation Link!")
        return redirect('user_registration')


def user_reset_password_confirm_view(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (DjangoUnicodeDecodeError, TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            uid = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, "Please Reset Your password")

            return redirect('user_reset_password')
            # messages.success(request, "Congratulations !your email is verified successfully!Now you can login your account")

        else:
            messages.error(request, "Invalid Password reset Link Or this link has been expired")
            return redirect('user_login')


def user_reset_password_view(request):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            uid = request.session.get('uid')
            if uid:
                print("uid: ", uid)
                user = CustomUser.objects.get(pk=uid)
                new_password = form.cleaned_data['new_password1']

                user.set_password(new_password)
                user.is_active = True
                user.save()
                messages.success(request, "Password reset successful")
                print("password: ", user.password)
                request.session['uid'] = None
                return redirect('user_login')
            else:
                messages.error(request, "invalid try")
                redirect('user_login')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'account/user_reset_password.html', {'PasswordResetForm': form})


def user_forgotten_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print("email: ", email)
            try:
                user = CustomUser.objects.get(email__exact=email)
                print("user:", user)
                # send a link in email to USER  , using this link user can reset his/her password
                current_site = get_current_site(request)
                message = render_to_string('account/password_reset_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                data = {
                    'subject': "Password reset link",
                    'body': message,
                    'to_email': email
                }

                Util.send_email(data)
                url = reverse('user_login') + f'?command=reset_password&email={email}'
                # messages.success(request, 'Thank you for registering with us! We are sent a email to your email address. Please verify your email.')
                return redirect(url)
            except CustomUser.DoesNotExist:
                messages.error(request,
                               "there is no account with this email [" + email + "]. Please write the correct email or create an account")
                return redirect('user_forgotten_password')
    else:
        form = PasswordResetForm()
    return render(request, 'account/user_forgotten_password.html', {'form': form})

# class PasswordResetView(PasswordResetView):
#     email_template_name = 'registration/password_reset_email.html'
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_sent')
#
#
# class PasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'registration/password_reset_done.html'
#
#
# class PasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'registration/password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')
#
#
# class PasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'registration/password_reset_complete.html'
