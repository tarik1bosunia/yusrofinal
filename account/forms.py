from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe


class PasswordInputWithToggle(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        toggle_html = '<div class="input-group-append"><button class="btn btn-outline-secondary" type="button" ' \
                      'onclick="togglePassword(this)"><i class="fa fa-eye"></i></button></div>'
        wrapper_html = '<div class="input-group">{input_html}{toggle_html}</div>'
        return mark_safe(wrapper_html.format(input_html=input_html, toggle_html=toggle_html))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Enter Your Email',
                'required': True,
            }
        )
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'Enter Your First Name',
                'required': True,
            }
        )
    )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'last_name',
                'placeholder': 'Enter Your Last Name',
                'required': True,
            }
        )
    )

    phone = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'phone',
                'placeholder': 'Enter Your Phone Number',
                'required': True,
            }
        )
    )
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=PasswordInputWithToggle(
            attrs={
                'class': 'form-control',
                'id': 'password1',
                'placeholder': 'Enter your password',
                'required': True,
            }
        )
    )
    password2 = forms.CharField(
        label='',
        strip=False,
        widget=PasswordInputWithToggle(
            attrs={
                'class': 'form-control',
                'id': 'password2',
                'placeholder': 'Enter Confirm password',
                'required': True,
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
        # labels = {'email': "Email"}


class EditUserForm(UserChangeForm):
    profile_image = forms.ImageField(required=False)
    password = None

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': 'autofocus', 'readonly': True})

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_image = self.cleaned_data.get('profile_image')

        if profile_image:
            user.profile_image = profile_image

        if commit:
            user.save()
        return user


class EditAdminForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Enter your email',
                'required': True,
            }
        )
    )
    password = forms.CharField(
        label='',
        strip=False,
        widget=PasswordInputWithToggle(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Enter your password',
                'required': True,
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
