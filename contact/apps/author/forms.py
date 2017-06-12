from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        # placeholder='Username',
        max_length=32
    )
    email = forms.CharField(
        required=True,
        label='Email',
        # placeholder='Email',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        # placeholder='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )


class UserSettingForm_api(forms.Form):
    api_key = forms.CharField(
        required=True,
        label='Enter new API key',
        max_length=128
    )


class UserSettingForm_pas(forms.Form):
    password = forms.CharField(
        required=True,
        label='Enter new password:',
        max_length=32,
        widget=forms.PasswordInput()
    )