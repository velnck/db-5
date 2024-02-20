from django.forms import ModelForm, CharField, PasswordInput

from users.models import Users


class RegisterForm(ModelForm):
    class Meta:
        model = Users
        widgets = {
            'password': PasswordInput(),
        }
        fields = ['username', 'password', 'email',
                  'phone_number', 'name']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id': 'register-username-field',
            'class': 'form-control',
            'placeholder': 'Enter username...'
        })
        self.fields['password'].widget.attrs.update({
            'id': 'password1',
            'class': 'form-control',
            'placeholder': 'Enter password...'
        })
        self.fields['email'].widget.attrs.update({
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'Enter email...'
        })
        self.fields['phone_number'].widget.attrs.update({
            'id': 'phone_number',
            'class': 'form-control',
            'placeholder': 'Enter phone number...'
        })
        self.fields['name'].widget.attrs.update({
            'id': 'name',
            'class': 'form-control',
            'placeholder': 'Enter name...'
        })


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'phone_number', 'email',]

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
