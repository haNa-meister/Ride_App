from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    gender = (
        ('m', 'male'),
        ('f', 'female'),
    )
    username = forms.CharField(label='username', max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='email address',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='sex', choices=gender)
