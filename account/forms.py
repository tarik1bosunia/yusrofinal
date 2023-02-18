from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
        labels = {'email': "Email"}


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

